# Silavater Skillset Deployer

Portable local skill-set deployment kit for OpenCode / Claude Code style agent environments.

This folder is intended to be copied into another project, then used from that project to deploy curated skill sets from local mirrored repositories.

## Contents

```text
silavater-skillset-deployer/
├─ README.md
├─ README.zh-TW.md
├─ THIRD_PARTY_NOTICES.md
├─ docs/
│  ├─ SKILL_CATALOG.md
│  └─ SKILL_CATALOG.zh-TW.md
├─ scripts/
│  ├─ Deploy-SkillSet.cmd
│  ├─ Deploy-SkillSet.ps1
│  ├─ Deploy-SkillSet-Py.cmd
│  ├─ Deploy-SkillSet.py
│  ├─ SkillDeployer-TUI.cmd
│  ├─ SkillDeployer-TUI.py
│  ├─ Update-SkillSources.cmd
│  └─ Update-SkillSources.py
└─ vendor/
   └─ skill-sources/
      ├─ mattpocock-skills/
      ├─ affaan-m-ecc/
      └─ ponytail/
```

## What each part does

- `vendor/skill-sources/` — local mirrors of upstream skill repositories. This is the offline/cacheable source of truth.
- `scripts/Deploy-SkillSet.py` — recommended deployer. It supports interactive selection, curated sets, individual skills, explicit target roots, and dry runs.
- `scripts/Deploy-SkillSet-Py.cmd` — Windows launcher for the Python deployer.
- `scripts/SkillDeployer-TUI.py` — two-mode terminal UI for `SkillSetDeployMode` and `SingleSkillDeployMode`.
- `scripts/SkillDeployer-TUI.cmd` — Windows launcher for the terminal UI.
- `scripts/Deploy-SkillSet.cmd` — legacy Windows launcher for the PowerShell implementation.
- `scripts/Deploy-SkillSet.ps1` — legacy PowerShell implementation that deploys curated skill sets from the local mirrors via `npx skills add`.
- `scripts/Update-SkillSources.py` — Python updater for the local mirrored upstream repositories.
- `scripts/Update-SkillSources.cmd` — Windows launcher for the Python updater.
- `docs/SKILL_CATALOG.md` — generated catalog of available skills, suggested skill sets, deployment commands, known caveats, and upstream source/license notes.
- `docs/SKILL_CATALOG.zh-TW.md` — Traditional Chinese catalog guide.
- `THIRD_PARTY_NOTICES.md` — third-party source, license, and local mirror notices.
- `README.md` — this portable usage guide.
- `README.zh-TW.md` — Traditional Chinese usage guide.

## Environment Requirements

Required for normal deployment:

- Windows is the primary supported environment for the included `.cmd` launchers.
- Python 3 must be available as either `py -3` or `python`.
- Node.js / npm must be installed, including `npx`.
- Network access is required the first time `npx skills` resolves the `skills` package.

Required for updating local mirrors:

- Git must be installed and available as `git`.
- Network access to GitHub is required when fetching or cloning the mirrored repositories.

Optional / legacy:

- PowerShell 5+ or PowerShell 7+ is only needed for the legacy `Deploy-SkillSet.ps1` deployer and catalog generation.

Quick environment check:

```cmd
py -3 --version
python --version
node --version
npm --version
npx --version
git --version
```

It is okay if only one of `py -3` or `python` works. The Windows launchers try `py -3` first, then `python`.

## Attribution / Upstream Sources

This project packages local mirrors and deployment helpers for selected agent skills from:

| Upstream | Description | License | Local path |
|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | Skills for real engineering workflows | MIT | `vendor/skill-sources/mattpocock-skills` |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | Cross-harness agent workflow system and skill catalog | MIT | `vendor/skill-sources/affaan-m-ecc` |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Skills-only mirror for YAGNI and over-engineering review workflows | MIT | `vendor/skill-sources/ponytail` |

The files under `vendor/skill-sources/` are mirrored from the upstream repositories above. This repository adds a portable deployment wrapper, curated skill sets, and documentation around those mirrored sources.

All upstream content remains the property of its respective authors and contributors. If you use, modify, or redistribute this repository, preserve the upstream license files and attribution notices. See `THIRD_PARTY_NOTICES.md` and the upstream `LICENSE` files for details.

## Disclaimer

This is an unofficial deployment package. It is not an official distribution of `mattpocock/skills`, `affaan-m/ECC`, or `DietrichGebert/ponytail`, and it is not affiliated with, endorsed by, or maintained by the upstream authors unless explicitly stated.

Ponytail is mirrored here as `SKILL.md` content only. This deployer does not install Ponytail's plugin package, lifecycle hooks, commands, or mode-tracking runtime; use the upstream Ponytail install flow if you want the full always-on plugin behavior.

For bug reports or feature requests about the original skills, refer to the upstream repositories. For issues with this packaging/deployment script, use this repository's issue tracker.

## Quick deploy from a target project

Recommended pattern: keep this package inside the target project, but run the deployer from the target project root. Project-scoped installs then land in the project, not in the deployer folder.

Before deploying, confirm the environment requirements above are available.

Fresh clones do not include `vendor/skill-sources/`. The TUI checks local mirrors on startup; if `vendor/` is missing, empty, or does not contain usable skill mirrors, it asks whether to run the updater before continuing.

Start from the target project root:

```cmd
cd "D:\projects\target-project"

# TUI with SkillSetDeployMode and SingleSkillDeployMode
.\silavater-skillset-deployer\scripts\SkillDeployer-TUI.cmd
```

For direct CLI use, bootstrap the local mirrors first when working from a fresh clone:

```cmd
cd "D:\projects\target-project\silavater-skillset-deployer"
.\scripts\Update-SkillSources.cmd
cd "D:\projects\target-project"

# Preview only; no changes
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --set env-setup --dry-run

# Install the environment setup set into the target project
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --set env-setup
```

The Python deployer uses its own `vendor/skill-sources/` as the source root. The target root defaults to the current directory. If you run from inside `silavater-skillset-deployer`, use `--target` to avoid installing into the deployer folder:

```cmd
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --target "D:\projects\target-project"
```

For project-scope installs, the Python deployer refuses to install into the deployer folder unless you pass `--allow-deployer-target`.

The script defaults to `--agent opencode`. To deploy to every supported agent surface:

```cmd
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --set env-setup --agent *
```

List available choices:

```cmd
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --list sets
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --list skills
```

Deploy individual skills without using the menu:

```cmd
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --skill matt:handoff --skill ecc:terminal-ops
```

Deployment modes:

| Mode | Command |
|---|---|
| TUI menu | `.\silavater-skillset-deployer\scripts\SkillDeployer-TUI.cmd` |
| Curated set | `.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --set env-setup` |
| Individual skills | `.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --skill matt:handoff --skill ecc:terminal-ops` |
| Explicit target | `.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --target "D:\projects\target-project"` |
| Preview only | `.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --set env-setup --dry-run` |

## Update local upstream mirrors

When the upstream skill repositories change, refresh all local mirrors with:

```cmd
.\scripts\Update-SkillSources.cmd
```

Requirements: Git and Python 3. On Windows, the `.cmd` launcher tries `py -3` first, then `python`.

Or call Python directly:

```cmd
py -3 .\scripts\Update-SkillSources.py
```

Preview the commands without network or file changes:

```cmd
.\scripts\Update-SkillSources.cmd --dry-run
```

Update only one mirror:

```cmd
.\scripts\Update-SkillSources.cmd --repo mattpocock-skills
.\scripts\Update-SkillSources.cmd --repo affaan-m-ecc
.\scripts\Update-SkillSources.cmd --repo ponytail
```

The updater manages:

- `vendor/skill-sources/mattpocock-skills` from `https://github.com/mattpocock/skills.git`
- `vendor/skill-sources/affaan-m-ecc` from `https://github.com/affaan-m/ECC.git`
- `vendor/skill-sources/ponytail` from `https://github.com/DietrichGebert/ponytail.git`, sparse-checkout to `skills/` plus `LICENSE`

It refuses to update a mirror with local changes, the wrong origin URL, a detached/wrong branch, or a diverged history. Git commands use a process-local `safe.directory` setting, so the script can handle copied Windows checkouts without changing global Git config.

If deploy fails with missing local skill sources, run this updater first. The `vendor/` directory is intentionally not tracked in this repository.

The TUI runs the same mirror checks automatically. On startup it offers to update missing or incomplete local mirrors, and if a deploy command fails later it offers to run the updater and retry once.

## Move into another project

Copy this whole folder into the target project:

```powershell
Copy-Item -Recurse -Force ".\silavater-skillset-deployer" "D:\projects\target-project\silavater-skillset-deployer"
```

Then run from inside the copied folder:

```cmd
cd "D:\projects\target-project\silavater-skillset-deployer"
.\scripts\Update-SkillSources.cmd
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --target "D:\projects\target-project" --dry-run
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --target "D:\projects\target-project"
```

Important: project scope installs into the target root. The Python deployer defaults that target to the current directory, but `--target` lets you make the destination explicit.

You can also skip the manual update step and launch the TUI from the target root; it will prompt to bootstrap mirrors if needed:

```cmd
cd "D:\projects\target-project"
.\silavater-skillset-deployer\scripts\SkillDeployer-TUI.cmd
```

## Recommended install pattern for target projects

For a target project root, use this structure:

```text
target-project/
└─ silavater-skillset-deployer/
   ├─ docs/SKILL_CATALOG.md
   ├─ scripts/SkillDeployer-TUI.cmd
   ├─ scripts/SkillDeployer-TUI.py
   ├─ scripts/Deploy-SkillSet-Py.cmd
   ├─ scripts/Deploy-SkillSet.py
   └─ vendor/skill-sources/...
```

Then:

```cmd
cd "D:\projects\target-project"
.\silavater-skillset-deployer\scripts\SkillDeployer-TUI.cmd
```

## Available curated sets

| Set | Purpose |
|---|---|
| `core-dev` | Daily development: code understanding, debugging, TDD, handoff, verification, plus Ponytail over-engineering review. |
| `lean-dev` | Anti-overengineering: YAGNI, minimal implementations, deletion-first reviews, and Ponytail debt tracking. |
| `env-setup` | Environment setup: CLI/package/workspace audit, docs lookup, safety guardrails. |
| `research` | Search-first research, source collection, docs lookup, decision summaries. |
| `security` | Secrets, MCPs, config, hooks, input boundaries, dangerous operation review. |
| `frontend` | React/Next, accessibility, performance, motion, UI polish. |
| `backend-ts` | TypeScript backend: API, DB, ORM, cache, Node/Next/Nest. |
| `python` | Python idioms, pytest, Django, data/ML workflows. |
| `agent-ops` | Skill scouting, stocktake, context, parallelism, local knowledge management. |
| `matt-all` | All primary Matt Pocock skills from the local mirror. |
| `ecc-all` | All primary ECC skills from the local mirror. |
| `pony-all` | All Ponytail `SKILL.md` skills from the skills-only mirror. |
| `all` | All primary skills from every mirror. |

Avoid `ecc-all` or `all` unless you intentionally want a very large active skill surface. Keep Ponytail's full plugin/hook behavior separate from this skills-only deployer.

## Refresh the catalog

Catalog generation is still handled by the legacy PowerShell implementation:

```cmd
.\scripts\Deploy-SkillSet.cmd -UpdateCatalog -DryRun
```

## Verify package health

```powershell
powershell -NoProfile -Command "[scriptblock]::Create((Get-Content -LiteralPath '.\scripts\Deploy-SkillSet.ps1' -Raw)) | Out-Null; 'parse-ok'"
.\scripts\Update-SkillSources.cmd --dry-run
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --dry-run
```

If you need the legacy PowerShell deployer, use the `.cmd` launcher or an explicit process-local bypass instead of changing system policy:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\Deploy-SkillSet.ps1 -Set env-setup -Scope project -DryRun
```

## Known caveat: `reasoning part 0 not found`

This is usually a session viewer / gateway / model fallback metadata parsing issue. It means a caller tried to read `reasoning[0]`, but the model response did not include a reasoning part. If the CLI commands finish and files are produced, it does not block this deployer.

## CC Switch

CC Switch is a separate environment/model/config switching tool. It is useful to evaluate later, but it is not a replacement for this local skill deployer.
