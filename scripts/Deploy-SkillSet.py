#!/usr/bin/env python3
"""Deploy curated or selected agent skills from local mirrored repositories."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


DEPLOYER_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_ROOT = DEPLOYER_ROOT / "vendor" / "skill-sources"
DEFAULT_BATCH_SIZE = 20

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


@dataclass(frozen=True)
class RepoSpec:
    key: str
    label: str
    path_name: str
    skill_pattern: re.Pattern[str]


@dataclass(frozen=True)
class SkillInfo:
    repo: RepoSpec
    name: str
    description: str
    path: Path


@dataclass(frozen=True)
class DeploySelection:
    description: str
    matt: tuple[str, ...] = ()
    ecc: tuple[str, ...] = ()


REPOS: dict[str, RepoSpec] = {
    "matt": RepoSpec(
        key="matt",
        label="mattpocock/skills",
        path_name="mattpocock-skills",
        skill_pattern=re.compile(
            r"^skills[\\/](engineering|productivity|misc)[\\/][^\\/]+[\\/]SKILL\.md$",
            re.IGNORECASE,
        ),
    ),
    "ecc": RepoSpec(
        key="ecc",
        label="affaan-m/ECC",
        path_name="affaan-m-ecc",
        skill_pattern=re.compile(r"^skills[\\/][^\\/]+[\\/]SKILL\.md$", re.IGNORECASE),
    ),
}


PREDEFINED_SETS: dict[str, DeploySelection] = {
    "core-dev": DeploySelection(
        description="Daily development: code understanding, debugging, TDD, handoff, and verification.",
        matt=("diagnosing-bugs", "tdd", "codebase-design", "handoff", "writing-great-skills"),
        ecc=("terminal-ops", "verification-loop", "git-workflow", "search-first", "tdd-workflow"),
    ),
    "env-setup": DeploySelection(
        description="Environment setup: CLI/package/workspace audit, docs lookup, and safety guardrails.",
        matt=("diagnosing-bugs", "codebase-design", "handoff"),
        ecc=("terminal-ops", "workspace-surface-audit", "research-ops", "search-first", "safety-guard", "security-scan"),
    ),
    "research": DeploySelection(
        description="Research: search first, collect sources, inspect docs, and produce decision summaries.",
        matt=("codebase-design", "grill-me", "handoff"),
        ecc=("research-ops", "search-first", "documentation-lookup", "market-research", "skill-scout"),
    ),
    "security": DeploySelection(
        description="Security review: secrets, MCPs, config files, hooks, input boundaries, and dangerous operations.",
        matt=("diagnosing-bugs", "git-guardrails-claude-code"),
        ecc=("security-review", "security-scan", "safety-guard", "gateguard", "llm-trading-agent-security"),
    ),
    "frontend": DeploySelection(
        description="Frontend/UI: React/Next, performance, accessibility, motion, and polish.",
        matt=("prototype", "tdd", "codebase-design"),
        ecc=(
            "frontend-patterns",
            "frontend-a11y",
            "react-patterns",
            "react-performance",
            "react-testing",
            "motion-foundations",
            "motion-patterns",
            "make-interfaces-feel-better",
            "vite-patterns",
        ),
    ),
    "backend-ts": DeploySelection(
        description="TypeScript backend: API, database, ORM, cache, Node/Next/Nest patterns.",
        matt=("diagnosing-bugs", "tdd", "codebase-design"),
        ecc=(
            "api-design",
            "backend-patterns",
            "nestjs-patterns",
            "prisma-patterns",
            "postgres-patterns",
            "redis-patterns",
            "mcp-server-patterns",
            "nodejs-keccak256",
        ),
    ),
    "python": DeploySelection(
        description="Python: idioms, pytest, Django, data, and ML workflows.",
        matt=("diagnosing-bugs", "tdd", "codebase-design"),
        ecc=("python-patterns", "python-testing", "django-patterns", "django-tdd", "django-verification", "mle-workflow", "pytorch-patterns"),
    ),
    "agent-ops": DeploySelection(
        description="Agent operations: skill scouting, stocktake, quality, context, parallelism, and local knowledge management.",
        matt=("writing-great-skills", "handoff", "grill-with-docs"),
        ecc=(
            "skill-scout",
            "skill-stocktake",
            "skill-comply",
            "knowledge-ops",
            "parallel-execution-optimizer",
            "strategic-compact",
            "iterative-retrieval",
            "workspace-surface-audit",
        ),
    ),
}


class DeployError(RuntimeError):
    pass


def repo_path(source_root: Path, repo: RepoSpec) -> Path:
    return source_root / repo.path_name


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def require_source_root(source_root: Path) -> None:
    problems: list[str] = []
    for repo in REPOS.values():
        path = repo_path(source_root, repo)
        if not path.exists():
            problems.append(f"{path} is missing")
        elif not path.is_dir():
            problems.append(f"{path} is not a directory")
        elif not any(path.rglob("SKILL.md")):
            problems.append(f"{path} does not contain any SKILL.md files")

    if problems:
        lines = ["Missing local skill sources:"]
        lines.extend(f"  - {problem}" for problem in problems)
        lines.extend(
            (
                "",
                "Fresh clones do not include vendor mirrors.",
                "Bootstrap or update them first:",
                f"  {DEPLOYER_ROOT / 'scripts' / 'Update-SkillSources.cmd'}",
            )
        )
        raise DeployError("\n".join(lines))


def parse_description(content: str) -> str:
    match = re.search(r"(?m)^description:\s*[\"']?(.*?)[\"']?\s*$", content)
    if match:
        return match.group(1).strip()

    for line in content.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed == "---" or trimmed.startswith("#"):
            continue
        if re.match(r"^[A-Za-z_-]+:\s*", trimmed):
            continue
        return trimmed

    return "No short description found in SKILL.md; inspect it before deploying."


def discover_skills(source_root: Path, repo: RepoSpec) -> list[SkillInfo]:
    root = repo_path(source_root, repo)
    if not root.exists():
        raise DeployError(f"Missing local skill source: {root}")

    skills: list[SkillInfo] = []
    for skill_file in root.rglob("SKILL.md"):
        relative = skill_file.relative_to(root)
        if not repo.skill_pattern.match(relative.as_posix()):
            continue

        content = skill_file.read_text(encoding="utf-8", errors="replace")
        skills.append(
            SkillInfo(
                repo=repo,
                name=skill_file.parent.name,
                description=parse_description(content),
                path=skill_file,
            )
        )

    return sorted(skills, key=lambda skill: skill.name.lower())


def all_skills(source_root: Path) -> dict[str, list[SkillInfo]]:
    return {key: discover_skills(source_root, repo) for key, repo in REPOS.items()}


def selection_from_set(set_name: str, source_root: Path) -> DeploySelection:
    if set_name in PREDEFINED_SETS:
        return PREDEFINED_SETS[set_name]

    skills = all_skills(source_root)
    if set_name == "matt-all":
        return DeploySelection("All Matt Pocock skills", matt=tuple(skill.name for skill in skills["matt"]))
    if set_name == "ecc-all":
        return DeploySelection("All ECC skills", ecc=tuple(skill.name for skill in skills["ecc"]))
    if set_name == "all":
        return DeploySelection(
            "All mirrored skills from both sources",
            matt=tuple(skill.name for skill in skills["matt"]),
            ecc=tuple(skill.name for skill in skills["ecc"]),
        )

    raise DeployError(f"Unknown set: {set_name}")


def selection_from_skills(skill_specs: Sequence[str], default_repo: str | None) -> DeploySelection:
    selected: dict[str, list[str]] = {"matt": [], "ecc": []}

    for spec in skill_specs:
        if ":" in spec:
            repo_key, skill_name = spec.split(":", 1)
            repo_key = normalize_repo_key(repo_key)
        elif default_repo:
            repo_key = normalize_repo_key(default_repo)
            skill_name = spec
        else:
            raise DeployError(f"Skill '{spec}' needs a repo prefix such as matt:{spec} or ecc:{spec}.")

        if repo_key == "both":
            raise DeployError("Use a concrete repo for single skills: matt or ecc.")
        if not skill_name:
            raise DeployError(f"Invalid skill spec: {spec}")
        selected[repo_key].append(skill_name)

    return DeploySelection(
        "Selected individual skills",
        matt=tuple(selected["matt"]),
        ecc=tuple(selected["ecc"]),
    )


def selection_from_repo_all(repo_key: str, source_root: Path) -> DeploySelection:
    normalized = normalize_repo_key(repo_key)
    if normalized == "both":
        return selection_from_set("all", source_root)
    if normalized == "matt":
        return selection_from_set("matt-all", source_root)
    return selection_from_set("ecc-all", source_root)


def normalize_repo_key(repo_key: str) -> str:
    value = repo_key.strip().lower()
    aliases = {
        "m": "matt",
        "mattpocock": "matt",
        "mattpocock-skills": "matt",
        "mattpocock/skills": "matt",
        "e": "ecc",
        "affaan": "ecc",
        "affaan-m-ecc": "ecc",
        "affaan-m/ecc": "ecc",
        "all": "both",
    }
    value = aliases.get(value, value)
    if value not in ("matt", "ecc", "both"):
        raise DeployError(f"Unknown repo: {repo_key}")
    return value


def validate_selection(selection: DeploySelection, source_root: Path) -> None:
    available = {
        key: {skill.name for skill in discover_skills(source_root, repo)}
        for key, repo in REPOS.items()
    }

    missing: list[str] = []
    for skill in selection.matt:
        if skill not in available["matt"]:
            missing.append(f"matt:{skill}")
    for skill in selection.ecc:
        if skill not in available["ecc"]:
            missing.append(f"ecc:{skill}")

    if missing:
        raise DeployError("Unknown skills in local mirrors: " + ", ".join(missing))


def batched(items: Sequence[str], size: int = DEFAULT_BATCH_SIZE) -> Iterable[Sequence[str]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def printable_command(args: Sequence[str]) -> str:
    return " ".join(f'"{part}"' if any(ch.isspace() for ch in part) else part for part in args)


def resolve_npx() -> str:
    candidates = ("npx.cmd", "npx.exe", "npx") if sys.platform == "win32" else ("npx",)
    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            return path

    raise DeployError(
        "Unable to find npx. Install Node.js/npm and confirm `npx --version` works in this terminal."
    )


def run_npx(args: Sequence[str], *, cwd: Path) -> None:
    command = list(args)
    command[0] = resolve_npx()
    result = subprocess.run(command, cwd=str(cwd))
    if result.returncode != 0:
        raise DeployError(f"Command failed with exit code {result.returncode}: {printable_command(command)}")


def invoke_skill_install(
    source_root: Path,
    target_root: Path,
    repo_key: str,
    skills: Sequence[str],
    *,
    scope: str,
    agent: str,
    dry_run: bool,
) -> None:
    if not skills:
        return

    source = repo_path(source_root, REPOS[repo_key])
    for batch in batched(tuple(skills)):
        args = ["npx", "skills", "add", str(source), "--copy", "-y"]
        if scope == "global":
            args.append("-g")
        if agent:
            args.extend(["--agent", agent])
        for skill in batch:
            args.extend(["--skill", skill])

        if dry_run:
            printable_args = list(args)
            try:
                printable_args[0] = resolve_npx()
            except DeployError:
                pass
            print(f"DRY RUN in {target_root}: {printable_command(printable_args)}")
        else:
            printable_args = list(args)
            printable_args[0] = resolve_npx()
            print(f"RUN in {target_root}: {printable_command(printable_args)}")
            run_npx(args, cwd=target_root)


def deploy_selection(
    selection: DeploySelection,
    *,
    source_root: Path,
    target_root: Path,
    scope: str,
    agent: str,
    dry_run: bool,
) -> None:
    if not selection.matt and not selection.ecc:
        raise DeployError("No skills selected.")

    validate_selection(selection, source_root)
    print(f"Selected: {selection.description}")
    print(f"Source root: {source_root}")
    print(f"Target root: {target_root}")
    print(f"Scope: {scope}")
    print(f"Agent: {agent or '(none)'}")

    invoke_skill_install(source_root, target_root, "matt", selection.matt, scope=scope, agent=agent, dry_run=dry_run)
    invoke_skill_install(source_root, target_root, "ecc", selection.ecc, scope=scope, agent=agent, dry_run=dry_run)


def prompt_choice(title: str, options: Sequence[tuple[str, str]]) -> str:
    print(f"\n{title}")
    for index, (_, label) in enumerate(options, start=1):
        print(f"  {index}. {label}")

    while True:
        raw = input("Choose a number: ").strip()
        if raw.isdigit():
            index = int(raw)
            if 1 <= index <= len(options):
                return options[index - 1][0]
        print("Invalid choice.")


def prompt_yes_no(message: str, *, default: bool = False) -> bool:
    suffix = "Y/n" if default else "y/N"
    raw = input(f"{message} [{suffix}]: ").strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes")


def format_skill_label(skill: SkillInfo) -> str:
    description = skill.description
    if len(description) > 90:
        description = description[:87].rstrip() + "..."
    return f"{skill.repo.key}:{skill.name} - {description}"


def choose_skills_interactively(source_root: Path) -> DeploySelection:
    skills_by_repo = all_skills(source_root)
    repo_choice = prompt_choice(
        "Choose skill source",
        (
            ("matt", "mattpocock/skills"),
            ("ecc", "affaan-m/ECC"),
            ("both", "Both"),
        ),
    )

    pool = []
    for key in ("matt", "ecc"):
        if repo_choice in (key, "both"):
            pool.extend(skills_by_repo[key])

    query = input("Search keyword (blank shows first 50): ").strip().lower()
    if query:
        pool = [
            skill
            for skill in pool
            if query in skill.name.lower() or query in skill.description.lower() or query in skill.repo.label.lower()
        ]

    if not pool:
        raise DeployError("No skills matched that search.")

    visible = pool[:50]
    print("\nChoose one or more skills by number. Use comma-separated values, for example: 1,3,4")
    for index, skill in enumerate(visible, start=1):
        print(f"  {index}. {format_skill_label(skill)}")
    if len(pool) > len(visible):
        print(f"  Showing first {len(visible)} of {len(pool)} matches. Search to narrow the list.")

    while True:
        raw = input("Skill numbers: ").strip()
        try:
            indexes = [int(part.strip()) for part in raw.split(",") if part.strip()]
        except ValueError:
            indexes = []
        if indexes and all(1 <= index <= len(visible) for index in indexes):
            break
        print("Invalid selection.")

    selected = {"matt": [], "ecc": []}
    for index in indexes:
        skill = visible[index - 1]
        selected[skill.repo.key].append(skill.name)

    return DeploySelection(
        "Selected individual skills",
        matt=tuple(selected["matt"]),
        ecc=tuple(selected["ecc"]),
    )


def choose_set_interactively(source_root: Path) -> DeploySelection:
    options = [(key, f"{key} - {selection.description}") for key, selection in PREDEFINED_SETS.items()]
    options.extend(
        (
            ("matt-all", "matt-all - All primary Matt Pocock skills"),
            ("ecc-all", "ecc-all - All primary ECC skills"),
            ("all", "all - All primary skills from both mirrors"),
        )
    )
    set_name = prompt_choice("Choose a curated set", options)
    return selection_from_set(set_name, source_root)


def choose_repo_all_interactively(source_root: Path) -> DeploySelection:
    repo_choice = prompt_choice(
        "Choose full source to deploy",
        (
            ("matt", "All Matt Pocock skills"),
            ("ecc", "All ECC skills"),
            ("both", "All skills from both mirrors"),
        ),
    )
    return selection_from_repo_all(repo_choice, source_root)


def interactive_selection(source_root: Path) -> DeploySelection:
    method = prompt_choice(
        "Choose deploy method",
        (
            ("set", "Curated skill set"),
            ("skill", "One or more individual skills"),
            ("all", "All skills from one source or both"),
        ),
    )
    if method == "set":
        return choose_set_interactively(source_root)
    if method == "skill":
        return choose_skills_interactively(source_root)
    return choose_repo_all_interactively(source_root)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deploy skills from this local deployer's mirrored skill sources."
    )
    parser.add_argument("--method", choices=("set", "skill", "all"), help="Deployment mode. Omit for interactive mode.")
    parser.add_argument("--set", choices=tuple(PREDEFINED_SETS.keys()) + ("matt-all", "ecc-all", "all"), help="Curated set to deploy.")
    parser.add_argument("--skill", action="append", default=[], help="Skill to deploy, such as matt:handoff or ecc:terminal-ops. Repeatable.")
    parser.add_argument("--repo", choices=("matt", "ecc", "both"), help="Repo for --skill without a prefix, or source for --method all.")
    parser.add_argument("--target", type=Path, default=Path.cwd(), help="Project root to install into. Defaults to the current directory.")
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT, help="Local skill-sources directory. Defaults to this deployer package.")
    parser.add_argument("--scope", choices=("project", "global"), default="project", help="Install scope for npx skills.")
    parser.add_argument("--agent", default="opencode", help="Agent argument passed to npx skills. Use '*' for all supported agents.")
    parser.add_argument("--dry-run", action="store_true", help="Print npx commands without running them.")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation for all-skill deployments.")
    parser.add_argument(
        "--allow-deployer-target",
        action="store_true",
        help="Allow project-scope installs into the deployer folder itself.",
    )
    parser.add_argument("--list", choices=("sets", "skills"), help="List available sets or skills, then exit.")
    return parser.parse_args(argv)


def print_sets() -> None:
    for key, selection in PREDEFINED_SETS.items():
        print(f"{key}: {selection.description}")
    print("matt-all: All primary Matt Pocock skills")
    print("ecc-all: All primary ECC skills")
    print("all: All primary skills from both mirrors")


def print_skills(source_root: Path) -> None:
    for key in ("matt", "ecc"):
        print(f"\n{REPOS[key].label}")
        for skill in discover_skills(source_root, REPOS[key]):
            print(f"  {skill.repo.key}:{skill.name} - {skill.description}")


def build_selection(args: argparse.Namespace, source_root: Path) -> DeploySelection:
    if args.set:
        return selection_from_set(args.set, source_root)
    if args.skill:
        return selection_from_skills(args.skill, args.repo)
    if args.method == "all":
        return selection_from_repo_all(args.repo or "both", source_root)
    if args.method == "set":
        return choose_set_interactively(source_root)
    if args.method == "skill":
        return choose_skills_interactively(source_root)
    if args.method is None:
        return interactive_selection(source_root)
    raise DeployError("No deployment selection was provided.")


def should_confirm_all(selection: DeploySelection) -> bool:
    return len(selection.matt) + len(selection.ecc) > 30


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    source_root = args.source_root.resolve()
    target_root = args.target.resolve()

    try:
        require_source_root(source_root)
        if args.list == "sets":
            print_sets()
            return 0
        if args.list == "skills":
            print_skills(source_root)
            return 0

        if not target_root.exists():
            raise DeployError(f"Target root does not exist: {target_root}")
        if (
            args.scope == "project"
            and not args.dry_run
            and not args.allow_deployer_target
            and is_relative_to(target_root, DEPLOYER_ROOT)
        ):
            raise DeployError(
                "Refusing to install into the deployer folder. "
                "Run this command from the target project root, pass --target <project-root>, "
                "or add --allow-deployer-target if this is intentional."
            )

        selection = build_selection(args, source_root)
        if should_confirm_all(selection) and not args.yes and not args.dry_run:
            count = len(selection.matt) + len(selection.ecc)
            if not prompt_yes_no(f"This will deploy {count} skills. Continue?"):
                print("Cancelled.")
                return 1

        deploy_selection(
            selection,
            source_root=source_root,
            target_root=target_root,
            scope=args.scope,
            agent=args.agent,
            dry_run=args.dry_run,
        )
    except (DeployError, KeyboardInterrupt) as error:
        print(f"\nERROR: {error}", file=sys.stderr)
        return 1

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
