#!/usr/bin/env python3
"""Update mirrored upstream skill repositories under vendor/skill-sources."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCES_ROOT = WORKSPACE_ROOT / "vendor" / "skill-sources"


@dataclass(frozen=True)
class RepoSpec:
    key: str
    label: str
    path: Path
    url: str
    branch: str = "main"
    sparse_paths: tuple[str, ...] = ()


REPOS: tuple[RepoSpec, ...] = (
    RepoSpec(
        key="mattpocock-skills",
        label="mattpocock/skills",
        path=SKILL_SOURCES_ROOT / "mattpocock-skills",
        url="https://github.com/mattpocock/skills.git",
    ),
    RepoSpec(
        key="affaan-m-ecc",
        label="affaan-m/ECC",
        path=SKILL_SOURCES_ROOT / "affaan-m-ecc",
        url="https://github.com/affaan-m/ECC.git",
    ),
    RepoSpec(
        key="ponytail",
        label="DietrichGebert/ponytail",
        path=SKILL_SOURCES_ROOT / "ponytail",
        url="https://github.com/DietrichGebert/ponytail.git",
        sparse_paths=("/skills/", "/LICENSE"),
    ),
)


class UpdateError(RuntimeError):
    pass


def run(
    args: Sequence[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        list(args),
        cwd=str(cwd) if cwd else None,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if check and result.returncode != 0:
        command = " ".join(args)
        details = (result.stderr or result.stdout or "").strip()
        raise UpdateError(f"Command failed ({result.returncode}): {command}\n{details}")
    return result


def git(repo: RepoSpec, args: Sequence[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    safe_directory = repo.path.resolve().as_posix()
    return run(
        [
            "git",
            "-c",
            f"safe.directory={safe_directory}",
            "-C",
            str(repo.path),
            *args,
        ],
        check=check,
    )


def printable_command(args: Sequence[str]) -> str:
    return " ".join(f'"{part}"' if any(ch.isspace() for ch in part) else part for part in args)


def sparse_checkout_command(repo: RepoSpec) -> list[str]:
    return ["git", "-C", str(repo.path), "sparse-checkout", "set", "--no-cone", *repo.sparse_paths]


def select_repos(selected: str) -> Iterable[RepoSpec]:
    if selected == "all":
        return REPOS
    return tuple(repo for repo in REPOS if repo.key == selected)


def ensure_git_available() -> None:
    run(["git", "--version"], check=True)


def clone_repo(repo: RepoSpec, *, dry_run: bool) -> None:
    if repo.path.exists():
        raise UpdateError(
            f"{repo.path} exists but is not a git checkout. Move it aside or restore a valid .git directory."
        )

    command = [
        "git",
        "clone",
        "--branch",
        repo.branch,
        "--single-branch",
    ]
    if repo.sparse_paths:
        command.extend(["--filter=blob:none", "--sparse"])
    command.extend([repo.url, str(repo.path)])

    sparse_command = sparse_checkout_command(repo)
    if dry_run:
        print(f"DRY RUN: {printable_command(command)}")
        if repo.sparse_paths:
            print(f"DRY RUN: {printable_command(sparse_command)}")
        return

    repo.path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Cloning {repo.label} into {repo.path}")
    run(command, check=True, capture=False)
    if repo.sparse_paths:
        print(f"Restricting {repo.label} checkout to: {', '.join(repo.sparse_paths)}")
        run(sparse_command, check=True, capture=False)


def require_clean_worktree(repo: RepoSpec) -> None:
    status = git(repo, ["status", "--porcelain"]).stdout.strip()
    if status:
        raise UpdateError(
            f"{repo.label} has local changes. Commit, stash, or discard them before updating:\n{status}"
        )


def verify_remote(repo: RepoSpec) -> None:
    remote = git(repo, ["remote", "get-url", "origin"]).stdout.strip()
    if remote != repo.url:
        raise UpdateError(
            f"{repo.label} origin URL mismatch.\n"
            f"Expected: {repo.url}\n"
            f"Actual:   {remote}"
        )


def verify_branch(repo: RepoSpec) -> None:
    branch = git(repo, ["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    if branch != repo.branch:
        raise UpdateError(
            f"{repo.label} is on branch '{branch}', expected '{repo.branch}'. "
            "Switch branches manually before updating."
        )


def ensure_sparse_checkout(repo: RepoSpec, *, dry_run: bool) -> None:
    if not repo.sparse_paths:
        return

    command = sparse_checkout_command(repo)
    if dry_run:
        print(f"DRY RUN: {printable_command(command)}")
        return

    print(f"Ensuring sparse checkout for {repo.label}: {', '.join(repo.sparse_paths)}")
    git(repo, ["sparse-checkout", "set", "--no-cone", *repo.sparse_paths])


def rev_parse(repo: RepoSpec, ref: str) -> str:
    return git(repo, ["rev-parse", "--short", ref]).stdout.strip()


def is_ancestor(repo: RepoSpec, older: str, newer: str) -> bool:
    result = git(repo, ["merge-base", "--is-ancestor", older, newer], check=False)
    if result.returncode in (0, 1):
        return result.returncode == 0
    details = (result.stderr or result.stdout or "").strip()
    raise UpdateError(f"Unable to compare {older} and {newer} for {repo.label}: {details}")


def update_repo(repo: RepoSpec, *, dry_run: bool) -> None:
    print(f"\n== {repo.label} ==")
    print(f"Path: {repo.path}")

    if not (repo.path / ".git").exists():
        clone_repo(repo, dry_run=dry_run)
        return

    require_clean_worktree(repo)
    verify_remote(repo)
    verify_branch(repo)
    ensure_sparse_checkout(repo, dry_run=dry_run)

    before = rev_parse(repo, "HEAD")
    remote_ref = f"origin/{repo.branch}"
    fetch_command = ["git", "-C", str(repo.path), "fetch", "--prune", "origin", repo.branch]
    merge_command = ["git", "-C", str(repo.path), "merge", "--ff-only", remote_ref]

    if dry_run:
        print(f"Current HEAD: {before}")
        print(f"DRY RUN: {printable_command(fetch_command)}")
        print(f"DRY RUN: {printable_command(merge_command)}")
        return

    print(f"Fetching {repo.branch} from origin")
    git(repo, ["fetch", "--prune", "origin", repo.branch])

    after_fetch = rev_parse(repo, remote_ref)
    if before == after_fetch:
        print(f"Already up to date at {before}")
        return

    if is_ancestor(repo, "HEAD", remote_ref):
        print(f"Fast-forwarding {before} -> {after_fetch}")
        git(repo, ["merge", "--ff-only", remote_ref])
        updated = rev_parse(repo, "HEAD")
        print(f"Updated to {updated}")
        return

    if is_ancestor(repo, remote_ref, "HEAD"):
        print(f"Local branch is ahead of origin/{repo.branch}; leaving it unchanged at {before}")
        return

    raise UpdateError(
        f"{repo.label} has diverged from {remote_ref}. Resolve the branch manually, then rerun this script."
    )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update the local mirrored skill source repositories."
    )
    parser.add_argument(
        "--repo",
        choices=["all", *(repo.key for repo in REPOS)],
        default="all",
        help="Which mirrored repository to update. Defaults to all.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the update commands without fetching, cloning, or merging.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    try:
        ensure_git_available()
        for repo in select_repos(args.repo):
            update_repo(repo, dry_run=args.dry_run)
    except UpdateError as error:
        print(f"\nERROR: {error}", file=sys.stderr)
        return 1

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
