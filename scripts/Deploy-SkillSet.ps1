# Deploy curated agent skill sets from local mirrored repositories.
# Sources are intentionally local so installs remain repeatable even if GitHub is unavailable.

[CmdletBinding()]
param(
    [ValidateSet(
        'core-dev',
        'lean-dev',
        'env-setup',
        'research',
        'security',
        'frontend',
        'backend-ts',
        'python',
        'agent-ops',
        'matt-all',
        'ecc-all',
        'pony-all',
        'all'
    )]
    [string]$Set = 'core-dev',

    [ValidateSet('project', 'global')]
    [string]$Scope = 'project',

    # Default to OpenCode for this workspace. Use '*' to link to all supported agents, or pass another agent name supported by `npx skills`.
    [string]$Agent = 'opencode',

    # Print install commands without executing them.
    [switch]$DryRun,

    # Regenerate docs/SKILL_CATALOG.md from local SKILL.md files before optionally installing.
    [switch]$UpdateCatalog
)

$ErrorActionPreference = 'Stop'

$WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$MattSource = Join-Path $WorkspaceRoot 'vendor\skill-sources\mattpocock-skills'
$EccSource = Join-Path $WorkspaceRoot 'vendor\skill-sources\affaan-m-ecc'
$PonySource = Join-Path $WorkspaceRoot 'vendor\skill-sources\ponytail'
$CatalogPath = Join-Path $WorkspaceRoot 'docs\SKILL_CATALOG.md'

function Assert-SourceExists {
    param([Parameter(Mandatory)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Missing local skill source: $Path. Clone/update mirrors under vendor\skill-sources first."
    }
}

function Get-RelativePathFromWorkspace {
    param([Parameter(Mandatory)][string]$Path)

    $fullWorkspace = [System.IO.Path]::GetFullPath($WorkspaceRoot).TrimEnd('\') + '\'
    $fullPath = [System.IO.Path]::GetFullPath($Path)
    if ($fullPath.StartsWith($fullWorkspace, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $fullPath.Substring($fullWorkspace.Length)
    }

    return $fullPath
}

function Get-SkillInfo {
    param(
        [Parameter(Mandatory)][string]$RepoName,
        [Parameter(Mandatory)][string]$Root
    )

    Assert-SourceExists -Path $Root

    $rootFull = [System.IO.Path]::GetFullPath($Root).TrimEnd('\\') + '\\'
    $skillFiles = Get-ChildItem -LiteralPath $Root -Filter 'SKILL.md' -Recurse -File |
        Where-Object {
            $relative = (Get-RelativePathFromWorkspace -Path $_.FullName) -replace '/', '\\'

            if ($RepoName -eq 'mattpocock/skills') {
                return $relative -match 'vendor\\skill-sources\\mattpocock-skills\\skills\\(engineering|productivity|misc)\\[^\\]+\\SKILL\.md$'
            }

            if ($RepoName -eq 'affaan-m/ECC') {
                return $relative -match 'vendor\\skill-sources\\affaan-m-ecc\\skills\\[^\\]+\\SKILL\.md$'
            }

            if ($RepoName -eq 'DietrichGebert/ponytail') {
                return $relative -match 'vendor\\skill-sources\\ponytail\\skills\\[^\\]+\\SKILL\.md$'
            }

            return $_.FullName.StartsWith($rootFull, [System.StringComparison]::OrdinalIgnoreCase)
        }

    foreach ($file in $skillFiles) {
        $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
        $name = Split-Path -Leaf (Split-Path -Parent $file.FullName)
        $relative = Get-RelativePathFromWorkspace -Path $file.FullName

        $description = $null
        if ($content -match '(?s)^\s*---\s*(.*?)\s*---') {
            $frontmatter = $Matches[1]
            if ($frontmatter -match '(?s)\bdescription:\s*(?:[>\|-]+\s*)?(.*?)(?:\s+\b(?:license|author|keywords|skills|commands):\s*|$)') {
                $description = (($Matches[1] -replace '\s+', ' ').Trim() -replace '^["'']|["'']$', '')
            }
        }

        if ($content -match '(?m)^description:\s*["'']?(.*?)["'']?\s*$') {
            $candidate = ($Matches[1].Trim() -replace '^["'']|["'']$', '')
            if ($candidate -and $candidate -notin @('>', '>-', '|', '|-')) {
                $description = $candidate
            }
        }

        if (-not $description) {
            $lines = $content -split "`r?`n"
            foreach ($line in $lines) {
                $trimmed = $line.Trim()
                if (-not $trimmed -or $trimmed -eq '---' -or $trimmed.StartsWith('#')) {
                    continue
                }
                if ($trimmed -match '^[A-Za-z_-]+:\s*') {
                    continue
                }
                $description = $trimmed
                break
            }
        }

        if (-not $description) {
            $description = 'No short description found in SKILL.md; inspect the linked file before deploying.'
        }

        [PSCustomObject]@{
            Repo        = $RepoName
            Name        = $name
            Description = ($description -replace '\|', '\/')
            Path        = $relative
        }
    }
}

function Get-PredefinedSets {
    return [ordered]@{
        'core-dev' = @{
            Description = 'Daily development: code understanding, debugging, TDD, handoff, and verification.'
            Matt = @('diagnosing-bugs', 'tdd', 'codebase-design', 'handoff', 'writing-great-skills')
            Ecc  = @('terminal-ops', 'verification-loop', 'git-workflow', 'search-first', 'tdd-workflow')
            Pony = @('ponytail-review')
        }
        'lean-dev' = @{
            Description = 'Anti-overengineering: YAGNI, minimal implementations, deletion-first reviews, and Ponytail debt tracking.'
            Matt = @()
            Ecc  = @()
            Pony = @('ponytail', 'ponytail-review', 'ponytail-audit', 'ponytail-debt', 'ponytail-help')
        }
        'env-setup' = @{
            Description = 'Environment setup: CLI/package/workspace audit, docs lookup, and safety guardrails.'
            Matt = @('diagnosing-bugs', 'codebase-design', 'handoff')
            Ecc  = @('terminal-ops', 'workspace-surface-audit', 'research-ops', 'search-first', 'safety-guard', 'security-scan')
            Pony = @()
        }
        'research' = @{
            Description = 'Research: search first, collect sources, inspect docs, and produce decision summaries.'
            Matt = @('codebase-design', 'grill-me', 'handoff')
            Ecc  = @('research-ops', 'search-first', 'documentation-lookup', 'market-research', 'skill-scout')
            Pony = @()
        }
        'security' = @{
            Description = 'Security review: secrets, MCPs, config files, hooks, input boundaries, and dangerous operations.'
            Matt = @('diagnosing-bugs', 'git-guardrails-claude-code')
            Ecc  = @('security-review', 'security-scan', 'safety-guard', 'gateguard', 'llm-trading-agent-security')
            Pony = @()
        }
        'frontend' = @{
            Description = 'Frontend/UI: React/Next, performance, accessibility, motion, and polish.'
            Matt = @('prototype', 'tdd', 'codebase-design')
            Ecc  = @('frontend-patterns', 'frontend-a11y', 'react-patterns', 'react-performance', 'react-testing', 'motion-foundations', 'motion-patterns', 'make-interfaces-feel-better', 'vite-patterns')
            Pony = @()
        }
        'backend-ts' = @{
            Description = 'TypeScript backend: API, database, ORM, cache, Node/Next/Nest patterns.'
            Matt = @('diagnosing-bugs', 'tdd', 'codebase-design')
            Ecc  = @('api-design', 'backend-patterns', 'nestjs-patterns', 'prisma-patterns', 'postgres-patterns', 'redis-patterns', 'mcp-server-patterns', 'nodejs-keccak256')
            Pony = @()
        }
        'python' = @{
            Description = 'Python: idioms, pytest, Django, data, and ML workflows.'
            Matt = @('diagnosing-bugs', 'tdd', 'codebase-design')
            Ecc  = @('python-patterns', 'python-testing', 'django-patterns', 'django-tdd', 'django-verification', 'mle-workflow', 'pytorch-patterns')
            Pony = @()
        }
        'agent-ops' = @{
            Description = 'Agent operations: skill scouting, stocktake, quality, context, parallelism, and local knowledge management.'
            Matt = @('writing-great-skills', 'handoff', 'grill-with-docs')
            Ecc  = @('skill-scout', 'skill-stocktake', 'skill-comply', 'knowledge-ops', 'parallel-execution-optimizer', 'strategic-compact', 'iterative-retrieval', 'workspace-surface-audit')
            Pony = @()
        }
    }
}

function Write-Catalog {
    $docsDir = Split-Path -Parent $CatalogPath
    if (-not (Test-Path -LiteralPath $docsDir)) {
        New-Item -ItemType Directory -Path $docsDir | Out-Null
    }

    $sets = Get-PredefinedSets
    $bt = [char]96
    $mattSkills = @(Get-SkillInfo -RepoName 'mattpocock/skills' -Root $MattSource | Sort-Object Name)
    $eccSkills = @(Get-SkillInfo -RepoName 'affaan-m/ECC' -Root $EccSource | Sort-Object Name)
    $ponySkills = @(Get-SkillInfo -RepoName 'DietrichGebert/ponytail' -Root $PonySource | Sort-Object Name)
    $allSkills = @($mattSkills + $eccSkills + $ponySkills)

    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.Add('# Local Skill Catalog')
    $lines.Add('')
    $lines.Add('Generated by `scripts/Deploy-SkillSet.cmd -UpdateCatalog -DryRun` from local mirrors.')
    $lines.Add('')
    $lines.Add('## Local Sources')
    $lines.Add('')
    $lines.Add('| Source | Local path | Count |')
    $lines.Add('|---|---:|---:|')
    $lines.Add("| mattpocock/skills | ${bt}vendor/skill-sources/mattpocock-skills${bt} | $($mattSkills.Count) |")
    $lines.Add("| affaan-m/ECC | ${bt}vendor/skill-sources/affaan-m-ecc${bt} | $($eccSkills.Count) |")
    $lines.Add("| DietrichGebert/ponytail | ${bt}vendor/skill-sources/ponytail${bt} | $($ponySkills.Count) |")
    $lines.Add("| Total | local mirror | $($allSkills.Count) |")
    $lines.Add('')
    $lines.Add('## Credits and Licenses')
    $lines.Add('')
    $lines.Add('This catalog references local mirrors of third-party skill repositories for offline and repeatable deployment:')
    $lines.Add('')
    $lines.Add('| Upstream | Local path | License |')
    $lines.Add('|---|---|---|')
    $lines.Add("| [mattpocock/skills](https://github.com/mattpocock/skills) | ${bt}vendor/skill-sources/mattpocock-skills${bt} | MIT |")
    $lines.Add("| [affaan-m/ECC](https://github.com/affaan-m/ECC) | ${bt}vendor/skill-sources/affaan-m-ecc${bt} | MIT |")
    $lines.Add("| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | ${bt}vendor/skill-sources/ponytail${bt} | MIT |")
    $lines.Add('')
    $lines.Add('The mirrored skill sources under `vendor/skill-sources/` are derived from those upstream projects. This repository is an independent and unofficial packaging/deployment helper and is not affiliated with, endorsed by, or maintained by the upstream authors unless explicitly stated.')
    $lines.Add('')
    $lines.Add('Please preserve upstream license files and attribution notices when using, modifying, or redistributing these mirrored sources. See `../THIRD_PARTY_NOTICES.md` and the upstream repositories for original source, documentation, history, and license terms.')
    $lines.Add('')
    $lines.Add('## Recommended Skill Sets')
    $lines.Add('')
    $lines.Add('> Recommendation: deploy only one or two sets at a time. Do not active-install all ECC skills or always-on style skills unless you explicitly want a larger agent surface. Full sources are already mirrored under `vendor/skill-sources/` and can be deployed on demand.')
    $lines.Add('')

    foreach ($key in $sets.Keys) {
        $set = $sets[$key]
        $lines.Add("### $key")
        $lines.Add('')
        $lines.Add($set.Description)
        $lines.Add('')
        $lines.Add("Deploy project scope:")
        $lines.Add('')
        $lines.Add('```cmd')
        $lines.Add(".\scripts\Deploy-SkillSet-Py.cmd --set $key")
        $lines.Add('```')
        $lines.Add('')
        $lines.Add('Skills:')
        $lines.Add('')
        $lines.Add('| Repo | Skills |')
        $lines.Add('|---|---|')
        if (@($set.Matt).Count -gt 0) {
            $lines.Add("| mattpocock/skills | $($set.Matt -join ', ') |")
        }
        if (@($set.Ecc).Count -gt 0) {
            $lines.Add("| affaan-m/ECC | $($set.Ecc -join ', ') |")
        }
        if (@($set.Pony).Count -gt 0) {
            $lines.Add("| DietrichGebert/ponytail | $($set.Pony -join ', ') |")
        }
        $lines.Add('')
    }

    $lines.Add('## Deployment Commands')
    $lines.Add('')
    $lines.Add('Use `scripts\Deploy-SkillSet-Py.cmd` on Windows for the Python deployer. It supports interactive selection, explicit `--target`, curated sets, individual skills, and dry runs.')
    $lines.Add('')
    $lines.Add('```cmd')
    $lines.Add('# Preview only')
    $lines.Add('.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --dry-run')
    $lines.Add('')
    $lines.Add('# Install a curated set into this workspace')
    $lines.Add('.\scripts\Deploy-SkillSet-Py.cmd --set env-setup')
    $lines.Add('')
    $lines.Add('# Install for every supported agent surface, not just OpenCode')
    $lines.Add('.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --agent *')
    $lines.Add('')
    $lines.Add('# Install a curated set globally')
    $lines.Add('.\scripts\Deploy-SkillSet-Py.cmd --set core-dev --scope global')
    $lines.Add('')
    $lines.Add('# Regenerate this catalog from local mirrors')
    $lines.Add('.\scripts\Deploy-SkillSet.cmd -UpdateCatalog -DryRun')
    $lines.Add('')
    $lines.Add('# Deploy individual skills')
    $lines.Add('.\scripts\Deploy-SkillSet-Py.cmd --skill matt:handoff --skill ecc:terminal-ops --skill pony:ponytail-review')
    $lines.Add('```')
    $lines.Add('')
    $lines.Add('## CC Switch Note')
    $lines.Add('')
    $lines.Add('CC Switch can be evaluated separately. It is closer to an environment/model/config switcher than a replacement for this skill catalog. Finish the local skill mirror and deployment script first, then add CC Switch to the `env-setup` workflow or a separate environment-switching task.')
    $lines.Add('')
    $lines.Add('## Known Issue: `reasoning part 0 not found`')
    $lines.Add('')
    $lines.Add('This is usually a session viewer / gateway / model fallback metadata parsing issue: the caller tries to read `reasoning[0]`, but the model response has no such part. If CLI commands finish and files are produced, it usually does not block skill mirroring or deployment. For debugging, check model names, fallback providers, the OpenCode session viewer, and whether the gateway supports reasoning parts.')
    $lines.Add('')
    $lines.Add('## Full Local Skill Catalog')
    $lines.Add('')
    $lines.Add('| Repo | Skill | Purpose | Local file |')
    $lines.Add('|---|---|---|---|')
    foreach ($skill in $allSkills) {
        $lines.Add("| $($skill.Repo) | ${bt}$($skill.Name)${bt} | $($skill.Description) | ${bt}$($skill.Path)${bt} |")
    }

    Set-Content -LiteralPath $CatalogPath -Value $lines -Encoding UTF8
    Write-Host "Catalog written: $CatalogPath"
}

function Get-SkillsForSet {
    param([Parameter(Mandatory)][string]$SetName)

    $sets = Get-PredefinedSets
    if ($sets.Contains($SetName)) {
        return $sets[$SetName]
    }

    if ($SetName -eq 'matt-all') {
        return @{ Description = 'All Matt Pocock skills'; Matt = @(Get-SkillInfo -RepoName 'mattpocock/skills' -Root $MattSource | Sort-Object Name | ForEach-Object Name); Ecc = @(); Pony = @() }
    }

    if ($SetName -eq 'ecc-all') {
        return @{ Description = 'All ECC skills'; Matt = @(); Ecc = @(Get-SkillInfo -RepoName 'affaan-m/ECC' -Root $EccSource | Sort-Object Name | ForEach-Object Name); Pony = @() }
    }

    if ($SetName -eq 'pony-all') {
        return @{ Description = 'All Ponytail skills'; Matt = @(); Ecc = @(); Pony = @(Get-SkillInfo -RepoName 'DietrichGebert/ponytail' -Root $PonySource | Sort-Object Name | ForEach-Object Name) }
    }

    if ($SetName -eq 'all') {
        return @{
            Description = 'All mirrored skills from all sources'
            Matt = @(Get-SkillInfo -RepoName 'mattpocock/skills' -Root $MattSource | Sort-Object Name | ForEach-Object Name)
            Ecc = @(Get-SkillInfo -RepoName 'affaan-m/ECC' -Root $EccSource | Sort-Object Name | ForEach-Object Name)
            Pony = @(Get-SkillInfo -RepoName 'DietrichGebert/ponytail' -Root $PonySource | Sort-Object Name | ForEach-Object Name)
        }
    }

    throw "Unknown set: $SetName"
}

function Invoke-SkillInstall {
    param(
        [Parameter(Mandatory)][string]$Source,
        [string[]]$Skills = @()
    )

    if (-not $Skills -or $Skills.Count -eq 0) {
        return
    }

    Assert-SourceExists -Path $Source

    $batchSize = 20
    for ($i = 0; $i -lt $Skills.Count; $i += $batchSize) {
        $batch = $Skills[$i..([Math]::Min($i + $batchSize - 1, $Skills.Count - 1))]
        $args = @('skills', 'add', $Source, '--copy', '-y')

        if ($Scope -eq 'global') {
            $args += '-g'
        }

        if ($Agent) {
            $args += @('--agent', $Agent)
        }

        foreach ($skill in $batch) {
            $args += @('--skill', $skill)
        }

        $printable = 'npx ' + (($args | ForEach-Object { if ($_ -match '\s') { '"' + $_ + '"' } else { $_ } }) -join ' ')
        if ($DryRun) {
            Write-Host "DRY RUN: $printable"
        } else {
            Write-Host "RUN: $printable"
            & npx @args
            if ($LASTEXITCODE -ne 0) {
                throw "skills install failed with exit code $LASTEXITCODE"
            }
        }
    }
}

Assert-SourceExists -Path $MattSource
Assert-SourceExists -Path $EccSource
Assert-SourceExists -Path $PonySource

if ($UpdateCatalog) {
    Write-Catalog
}

$selected = Get-SkillsForSet -SetName $Set
Write-Host "Selected set: $Set - $($selected.Description)"
Invoke-SkillInstall -Source $MattSource -Skills @($selected.Matt)
Invoke-SkillInstall -Source $EccSource -Skills @($selected.Ecc)
Invoke-SkillInstall -Source $PonySource -Skills @($selected.Pony)
