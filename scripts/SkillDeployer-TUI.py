#!/usr/bin/env python3
"""Small stdlib TUI for deploying skill sets or a single skill."""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
DEPLOYER_ROOT = SCRIPT_DIR.parent
DEPLOY_SCRIPT = SCRIPT_DIR / "Deploy-SkillSet.py"
UPDATE_SCRIPT = SCRIPT_DIR / "Update-SkillSources.py"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


class TuiError(RuntimeError):
    pass


class QuitRequested(RuntimeError):
    pass


@dataclass(frozen=True)
class SkillChoice:
    repo: str
    name: str
    description: str


@dataclass(frozen=True)
class DeployOptions:
    target: Path
    scope: str
    agent: str
    dry_run: bool


def load_deployer_module():
    spec = importlib.util.spec_from_file_location("skill_deployer", DEPLOY_SCRIPT)
    if spec is None or spec.loader is None:
        raise TuiError(f"Unable to load deployer script: {DEPLOY_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


DEPLOYER = load_deployer_module()


def clear_screen() -> None:
    command = "cls" if sys.platform == "win32" else "clear"
    subprocess.run(command, shell=True)


def pause() -> None:
    input("\nPress Enter to continue...")


def print_header(title: str) -> None:
    clear_screen()
    print("Silavater Skill Deployer")
    print("=" * 26)
    print(title)
    print("-" * len(title))


def ask_choice(title: str, options: Sequence[tuple[str, str]], *, allow_back: bool = True) -> str:
    while True:
        print(f"\n{title}")
        for index, (_, label) in enumerate(options, start=1):
            print(f"  {index}. {label}")
        if allow_back:
            print("  b. Back")
        print("  q. Quit")

        answer = input("Choose: ").strip().lower()
        if answer == "q":
            raise QuitRequested
        if allow_back and answer == "b":
            return "back"
        if answer.isdigit():
            index = int(answer)
            if 1 <= index <= len(options):
                return options[index - 1][0]
        print("Invalid choice.")


def ask_text(prompt: str, *, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    answer = input(f"{prompt}{suffix}: ").strip()
    if not answer and default is not None:
        return default
    return answer


def ask_yes_no(prompt: str, *, default: bool = False) -> bool:
    suffix = "Y/n" if default else "y/N"
    answer = input(f"{prompt} [{suffix}]: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def check_command(command: str) -> str:
    path = shutil.which(command)
    if not path:
        return "missing"
    try:
        result = subprocess.run([command, "--version"], text=True, capture_output=True, timeout=5)
    except Exception:
        return "found"
    output = (result.stdout or result.stderr or "").strip().splitlines()
    return output[0] if output else "found"


def check_python() -> str:
    py_launcher = shutil.which("py")
    if py_launcher:
        result = subprocess.run(["py", "-3", "--version"], text=True, capture_output=True)
        if result.returncode == 0:
            return (result.stdout or result.stderr).strip()

    python = shutil.which("python")
    if python:
        result = subprocess.run(["python", "--version"], text=True, capture_output=True)
        if result.returncode == 0:
            return (result.stdout or result.stderr).strip()

    return "missing"


def source_problem_labels() -> list[str]:
    problems: list[str] = []
    vendor_root = DEPLOYER_ROOT / "vendor"
    source_root = DEPLOYER.DEFAULT_SOURCE_ROOT

    if not vendor_root.exists():
        problems.append(f"vendor folder is missing: {vendor_root}")
    elif not vendor_root.is_dir():
        problems.append(f"vendor path is not a directory: {vendor_root}")

    if not source_root.exists():
        problems.append(f"skill-sources folder is missing: {source_root}")
        return problems
    if not source_root.is_dir():
        problems.append(f"skill-sources path is not a directory: {source_root}")
        return problems

    for repo in DEPLOYER.REPOS.values():
        path = DEPLOYER.repo_path(source_root, repo)
        if not path.exists():
            problems.append(f"{repo.label} mirror is missing: {path}")
        elif not path.is_dir():
            problems.append(f"{repo.label} mirror path is not a directory: {path}")
        elif not any(path.rglob("SKILL.md")):
            problems.append(f"{repo.label} mirror contains no SKILL.md files: {path}")

    return problems


def show_environment_status() -> None:
    print_header("Environment")
    source_problems = source_problem_labels()
    checks = (
        ("Python", check_python()),
        ("Node.js", check_command("node")),
        ("npm", check_command("npm")),
        ("npx", check_command("npx")),
        ("Git", check_command("git")),
        ("Mirrors", "ok" if not source_problems else "needs update"),
    )
    for name, status in checks:
        print(f"{name:12} {status}")
    if source_problems:
        print("\nMirror issues:")
        for problem in source_problems:
            print(f"- {problem}")
    pause()


def run_update_sources() -> None:
    print("\nRunning source update:")
    print(f"{sys.executable} {UPDATE_SCRIPT}")
    result = subprocess.run([sys.executable, str(UPDATE_SCRIPT)])
    if result.returncode != 0:
        raise TuiError(f"Source update failed with exit code {result.returncode}")


def ensure_local_sources() -> None:
    problems = source_problem_labels()
    if not problems:
        return

    print_header("Local Mirrors Need Update")
    print("Fresh clones do not include vendor mirrors.")
    print("The deployer needs local skill sources before it can install skills.\n")
    for problem in problems:
        print(f"- {problem}")

    print("\nThis will run:")
    print(f"{sys.executable} {UPDATE_SCRIPT}")
    if not ask_yes_no("Bootstrap/update local mirrors now", default=True):
        raise TuiError(
            "Local mirrors are missing. Run scripts\\Update-SkillSources.cmd from the deployer folder, then rerun the TUI."
        )

    run_update_sources()

    remaining = source_problem_labels()
    if remaining:
        raise TuiError("Local mirrors are still incomplete after update:\n" + "\n".join(f"- {item}" for item in remaining))


def is_inside_deployer(path: Path) -> bool:
    try:
        path.resolve().relative_to(DEPLOYER_ROOT.resolve())
        return True
    except ValueError:
        return False


def ask_common_options() -> DeployOptions:
    print("\nDeployment options")
    target_raw = ask_text("Target project root", default=str(Path.cwd()))
    target = Path(target_raw).expanduser().resolve()
    while not target.exists():
        print(f"Target does not exist: {target}")
        target = Path(ask_text("Target project root", default=str(Path.cwd()))).expanduser().resolve()

    scope = ask_choice(
        "Install scope",
        (("project", "project"), ("global", "global")),
        allow_back=False,
    )
    agent = ask_text("Agent", default="opencode")
    dry_run = ask_yes_no("Preview only / dry-run", default=True)

    if scope == "project" and not dry_run and is_inside_deployer(target):
        print("\nThe selected target is inside the deployer package.")
        print("Use a real project root, or run Deploy-SkillSet.py with --allow-deployer-target if intentional.")
        raise TuiError("Refusing to deploy into the deployer folder.")

    return DeployOptions(target=target, scope=scope, agent=agent, dry_run=dry_run)


def command_for_skill_set(set_name: str, options: DeployOptions) -> list[str]:
    command = [
        sys.executable,
        str(DEPLOY_SCRIPT),
        "--set",
        set_name,
        "--target",
        str(options.target),
        "--scope",
        options.scope,
        "--agent",
        options.agent,
    ]
    if options.dry_run:
        command.append("--dry-run")
    return command


def command_for_single_skill(skill: SkillChoice, options: DeployOptions) -> list[str]:
    command = [
        sys.executable,
        str(DEPLOY_SCRIPT),
        "--skill",
        f"{skill.repo}:{skill.name}",
        "--target",
        str(options.target),
        "--scope",
        options.scope,
        "--agent",
        options.agent,
    ]
    if options.dry_run:
        command.append("--dry-run")
    return command


def print_review(command: Sequence[str], summary: Sequence[tuple[str, str]]) -> bool:
    print("\nReview")
    for label, value in summary:
        print(f"{label:14} {value}")
    print("\nCommand")
    print(" ".join(f'"{part}"' if " " in part else part for part in command))
    return ask_yes_no("Run this command", default=False)


def run_command(command: Sequence[str]) -> None:
    result = subprocess.run(list(command))
    if result.returncode == 0:
        return

    print(f"\nDeploy command failed with exit code {result.returncode}.")
    if not ask_yes_no("Run source update and retry once", default=True):
        raise TuiError(f"Deploy command failed with exit code {result.returncode}")

    run_update_sources()
    retry = subprocess.run(list(command))
    if retry.returncode != 0:
        raise TuiError(f"Deploy command still failed after update with exit code {retry.returncode}")


def skill_set_deploy_mode() -> None:
    ensure_local_sources()
    while True:
        print_header("SkillSetDeployMode")
        set_options = [(name, f"{name} - {selection.description}") for name, selection in DEPLOYER.PREDEFINED_SETS.items()]
        set_name = ask_choice("Choose a skill set", set_options)
        if set_name == "back":
            return

        options = ask_common_options()
        command = command_for_skill_set(set_name, options)
        summary = (
            ("Mode", "SkillSetDeployMode"),
            ("Skill set", set_name),
            ("Target", str(options.target)),
            ("Scope", options.scope),
            ("Agent", options.agent),
            ("Dry-run", str(options.dry_run)),
        )
        if print_review(command, summary):
            run_command(command)
            pause()
            return


def collect_skills() -> list[SkillChoice]:
    skills_by_repo = DEPLOYER.all_skills(DEPLOYER.DEFAULT_SOURCE_ROOT)
    choices: list[SkillChoice] = []
    for repo_key in ("matt", "ecc"):
        for skill in skills_by_repo[repo_key]:
            choices.append(SkillChoice(repo=repo_key, name=skill.name, description=skill.description))
    return sorted(choices, key=lambda item: (item.repo, item.name.lower()))


def short_description(text: str, limit: int = 84) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def single_skill_deploy_mode() -> None:
    ensure_local_sources()
    skills = collect_skills()
    while True:
        print_header("SingleSkillDeployMode")
        repo_filter = ask_choice(
            "Choose skill source",
            (("all", "all"), ("matt", "mattpocock/skills"), ("ecc", "affaan-m/ECC")),
        )
        if repo_filter == "back":
            return

        query = ask_text("Search keyword", default="")
        query_lower = query.lower()
        filtered = [
            skill
            for skill in skills
            if (repo_filter == "all" or skill.repo == repo_filter)
            and (not query_lower or query_lower in skill.name.lower() or query_lower in skill.description.lower())
        ]
        if not filtered:
            print("No skills matched that filter.")
            pause()
            continue

        visible = filtered[:40]
        skill_options = [
            (f"{skill.repo}:{skill.name}", f"{skill.repo}:{skill.name} - {short_description(skill.description)}")
            for skill in visible
        ]
        if len(filtered) > len(visible):
            print(f"\nShowing first {len(visible)} of {len(filtered)} matches. Search to narrow the list.")

        selected = ask_choice("Choose one skill", skill_options)
        if selected == "back":
            continue

        repo, name = selected.split(":", 1)
        skill = next(item for item in visible if item.repo == repo and item.name == name)
        options = ask_common_options()
        command = command_for_single_skill(skill, options)
        summary = (
            ("Mode", "SingleSkillDeployMode"),
            ("Skill", f"{skill.repo}:{skill.name}"),
            ("Target", str(options.target)),
            ("Scope", options.scope),
            ("Agent", options.agent),
            ("Dry-run", str(options.dry_run)),
        )
        if print_review(command, summary):
            run_command(command)
            pause()
            return


def main() -> int:
    try:
        ensure_local_sources()
        while True:
            print_header("Main Menu")
            mode = ask_choice(
                "Choose deploy mode",
                (
                    ("set", "SkillSetDeployMode"),
                    ("single", "SingleSkillDeployMode"),
                ),
                allow_back=False,
            )
            if mode == "set":
                skill_set_deploy_mode()
            elif mode == "single":
                single_skill_deploy_mode()
    except QuitRequested:
        print("\nGoodbye.")
        return 0
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
        return 0
    except TuiError as error:
        print(f"\nERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
