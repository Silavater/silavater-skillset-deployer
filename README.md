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
│  ├─ Update-SkillSources.cmd
│  └─ Update-SkillSources.py
└─ vendor/
   └─ skill-sources/
      ├─ mattpocock-skills/
      └─ affaan-m-ecc/
```

## What each part does

- `vendor/skill-sources/` — local mirrors of upstream skill repositories. This is the offline/cacheable source of truth.
- `scripts/Deploy-SkillSet.cmd` — recommended Windows launcher. It calls the PowerShell implementation with a process-local execution-policy bypass, so copied unsigned scripts can run without changing machine policy.
- `scripts/Deploy-SkillSet.ps1` — PowerShell implementation that deploys curated skill sets from the local mirrors via `npx skills add`.
- `scripts/Update-SkillSources.py` — Python updater for the two local mirrored upstream repositories.
- `scripts/Update-SkillSources.cmd` — Windows launcher for the Python updater.
- `docs/SKILL_CATALOG.md` — generated catalog of available skills, suggested skill sets, deployment commands, known caveats, and upstream source/license notes.
- `docs/SKILL_CATALOG.zh-TW.md` — Traditional Chinese catalog guide.
- `THIRD_PARTY_NOTICES.md` — third-party source, license, and local mirror notices.
- `README.md` — this portable usage guide.
- `README.zh-TW.md` — Traditional Chinese usage guide.

## Attribution / Upstream Sources

This project packages local mirrors and deployment helpers for selected agent skills from:

| Upstream | Description | License | Local path |
|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | Skills for real engineering workflows | MIT | `vendor/skill-sources/mattpocock-skills` |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | Cross-harness agent workflow system and skill catalog | MIT | `vendor/skill-sources/affaan-m-ecc` |

The files under `vendor/skill-sources/` are mirrored from the upstream repositories above. This repository adds a portable deployment wrapper, curated skill sets, and documentation around those mirrored sources.

All upstream content remains the property of its respective authors and contributors. If you use, modify, or redistribute this repository, preserve the upstream license files and attribution notices. See `THIRD_PARTY_NOTICES.md` and the upstream `LICENSE` files for details.

## Disclaimer

This is an unofficial deployment package. It is not an official distribution of `mattpocock/skills` or `affaan-m/ECC`, and it is not affiliated with, endorsed by, or maintained by the upstream authors unless explicitly stated.

For bug reports or feature requests about the original skills, refer to the upstream repositories. For issues with this packaging/deployment script, use this repository's issue tracker.

## Quick use inside this folder

From inside `silavater-skillset-deployer`:

```cmd
# Preview only; no changes
.\scripts\Deploy-SkillSet.cmd -Set env-setup -Scope project -DryRun

# Install the environment setup set into this project
.\scripts\Deploy-SkillSet.cmd -Set env-setup -Scope project
```

Use the `.cmd` launcher on Windows unless you intentionally want to call PowerShell yourself. It avoids the common `Deploy-SkillSet.ps1 is not digitally signed` / `PSSecurityException` failure without permanently relaxing your system execution policy.

The script defaults to `-Agent opencode`. To deploy to every supported agent surface:

```cmd
.\scripts\Deploy-SkillSet.cmd -Set env-setup -Scope project -Agent *
```

## Update local upstream mirrors

When the upstream skill repositories change, refresh both local mirrors with:

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
```

The updater manages:

- `vendor/skill-sources/mattpocock-skills` from `https://github.com/mattpocock/skills.git`
- `vendor/skill-sources/affaan-m-ecc` from `https://github.com/affaan-m/ECC.git`

It refuses to update a mirror with local changes, the wrong origin URL, a detached/wrong branch, or a diverged history. Git commands use a process-local `safe.directory` setting, so the script can handle copied Windows checkouts without changing global Git config.

## Move into another project

Copy this whole folder into the target project:

```powershell
Copy-Item -Recurse -Force ".\silavater-skillset-deployer" "D:\projects\target-project\silavater-skillset-deployer"
```

Then run from inside the copied folder:

```cmd
cd "D:\projects\target-project\silavater-skillset-deployer"
.\scripts\Deploy-SkillSet.cmd -Set env-setup -Scope project -DryRun
.\scripts\Deploy-SkillSet.cmd -Set env-setup -Scope project
```

Important: `-Scope project` installs relative to the current directory. If you run the script from inside `silavater-skillset-deployer`, the skills are installed into that folder's project surface. If you want skills installed at the target project root, copy the `vendor/`, `scripts/`, and `docs/` folders from this package into the target root, then run the script there.

## Recommended install pattern for target projects

For a target project root, use this structure:

```text
target-project/
├─ docs/SKILL_CATALOG.md
├─ scripts/Deploy-SkillSet.cmd
├─ scripts/Deploy-SkillSet.ps1
└─ vendor/skill-sources/...
```

Then:

```cmd
cd "D:\projects\target-project"
.\scripts\Deploy-SkillSet.cmd -Set env-setup -Scope project -DryRun
.\scripts\Deploy-SkillSet.cmd -Set env-setup -Scope project
```

## Available curated sets

| Set | Purpose |
|---|---|
| `core-dev` | Daily development: code understanding, debugging, TDD, handoff, verification. |
| `env-setup` | Environment setup: CLI/package/workspace audit, docs lookup, safety guardrails. |
| `research` | Search-first research, source collection, docs lookup, decision summaries. |
| `security` | Secrets, MCPs, config, hooks, input boundaries, dangerous operation review. |
| `frontend` | React/Next, accessibility, performance, motion, UI polish. |
| `backend-ts` | TypeScript backend: API, DB, ORM, cache, Node/Next/Nest. |
| `python` | Python idioms, pytest, Django, data/ML workflows. |
| `agent-ops` | Skill scouting, stocktake, context, parallelism, local knowledge management. |
| `matt-all` | All primary Matt Pocock skills from the local mirror. |
| `ecc-all` | All primary ECC skills from the local mirror. |
| `all` | All primary skills from both mirrors. |

Avoid `ecc-all` or `all` unless you intentionally want a very large active skill surface.

## Refresh the catalog

```cmd
.\scripts\Deploy-SkillSet.cmd -UpdateCatalog -DryRun
```

## Verify package health

```powershell
powershell -NoProfile -Command "[scriptblock]::Create((Get-Content -LiteralPath '.\scripts\Deploy-SkillSet.ps1' -Raw)) | Out-Null; 'parse-ok'"
.\scripts\Update-SkillSources.cmd --dry-run
.\scripts\Deploy-SkillSet.cmd -Set env-setup -Scope project -DryRun
```

If you prefer direct PowerShell invocation, use an explicit process-local bypass instead of changing system policy:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\Deploy-SkillSet.ps1 -Set env-setup -Scope project -DryRun
```

## Known caveat: `reasoning part 0 not found`

This is usually a session viewer / gateway / model fallback metadata parsing issue. It means a caller tried to read `reasoning[0]`, but the model response did not include a reasoning part. If the CLI commands finish and files are produced, it does not block this deployer.

## CC Switch

CC Switch is a separate environment/model/config switching tool. It is useful to evaluate later, but it is not a replacement for this local skill deployer.
