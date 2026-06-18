# 本機技能目錄 / Local Skill Catalog

此檔目前同步自最新英文 catalog，以確保 skill 名稱、數量與本機路徑準確。Skill 描述保留上游原文，避免翻譯後改變觸發語意。

由 `scripts/Deploy-SkillSet.cmd -UpdateCatalog -DryRun` 根據本機 mirrors 產生。

## 本機來源 / Local Sources

| Source | Local path | Count |
|---|---:|---:|
| mattpocock/skills | `vendor/skill-sources/mattpocock-skills` | 23 |
| affaan-m/ECC | `vendor/skill-sources/affaan-m-ecc` | 271 |
| DietrichGebert/ponytail | `vendor/skill-sources/ponytail` | 5 |
| Total | local mirror | 299 |

## 來源與授權 / Credits and Licenses

此目錄引用第三方 skill repositories 的本機 mirrors，以支援離線且可重複的部署：

| Upstream | Local path | License |
|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | `vendor/skill-sources/mattpocock-skills` | MIT |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | `vendor/skill-sources/affaan-m-ecc` | MIT |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | `vendor/skill-sources/ponytail` | MIT |

`vendor/skill-sources/` 底下的 mirrored skill sources 來自上述上游專案。本 repository 是獨立且非官方的打包／部署輔助工具；除非另有明確說明，否則不代表受到上游作者認可、背書或維護。

使用、修改或重新散布這些 mirrored sources 時，請保留上游 license files 與 attribution notices。原始來源、文件、歷史與授權條款請見 `../THIRD_PARTY_NOTICES.md` 與各上游 repository。

## 建議技能集 / Recommended Skill Sets

> 建議：一次只部署一到兩組 skill set。除非你明確想要更大的 agent surface，否則不要 active-install 全部 ECC skills 或 always-on 風格 skills。完整來源已 mirror 到 `vendor/skill-sources/`，需要時再按需部署。

### core-dev

日常開發：程式碼理解、除錯、TDD、交接、驗證，並加入 Ponytail over-engineering review。

Deploy project scope:

```cmd
.\scripts\Deploy-SkillSet-Py.cmd --set core-dev
```

Skills:

| Repo | Skills |
|---|---|
| mattpocock/skills | diagnosing-bugs, tdd, codebase-design, handoff, writing-great-skills |
| affaan-m/ECC | terminal-ops, verification-loop, git-workflow, search-first, tdd-workflow |
| DietrichGebert/ponytail | ponytail-review |

### lean-dev

反過度工程：YAGNI、最小可行實作、以刪減優先的 review 與 Ponytail debt 追蹤。

Deploy project scope:

```cmd
.\scripts\Deploy-SkillSet-Py.cmd --set lean-dev
```

Skills:

| Repo | Skills |
|---|---|
| DietrichGebert/ponytail | ponytail, ponytail-review, ponytail-audit, ponytail-debt, ponytail-help |

### env-setup

Environment setup: CLI/package/workspace audit, docs lookup, and safety guardrails.

Deploy project scope:

```cmd
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup
```

Skills:

| Repo | Skills |
|---|---|
| mattpocock/skills | diagnosing-bugs, codebase-design, handoff |
| affaan-m/ECC | terminal-ops, workspace-surface-audit, research-ops, search-first, safety-guard, security-scan |

### research

Research: search first, collect sources, inspect docs, and produce decision summaries.

Deploy project scope:

```cmd
.\scripts\Deploy-SkillSet-Py.cmd --set research
```

Skills:

| Repo | Skills |
|---|---|
| mattpocock/skills | codebase-design, grill-me, handoff |
| affaan-m/ECC | research-ops, search-first, documentation-lookup, market-research, skill-scout |

### security

Security review: secrets, MCPs, config files, hooks, input boundaries, and dangerous operations.

Deploy project scope:

```cmd
.\scripts\Deploy-SkillSet-Py.cmd --set security
```

Skills:

| Repo | Skills |
|---|---|
| mattpocock/skills | diagnosing-bugs, git-guardrails-claude-code |
| affaan-m/ECC | security-review, security-scan, safety-guard, gateguard, llm-trading-agent-security |

### frontend

Frontend/UI: React/Next, performance, accessibility, motion, and polish.

Deploy project scope:

```cmd
.\scripts\Deploy-SkillSet-Py.cmd --set frontend
```

Skills:

| Repo | Skills |
|---|---|
| mattpocock/skills | prototype, tdd, codebase-design |
| affaan-m/ECC | frontend-patterns, frontend-a11y, react-patterns, react-performance, react-testing, motion-foundations, motion-patterns, make-interfaces-feel-better, vite-patterns |

### backend-ts

TypeScript backend: API, database, ORM, cache, Node/Next/Nest patterns.

Deploy project scope:

```cmd
.\scripts\Deploy-SkillSet-Py.cmd --set backend-ts
```

Skills:

| Repo | Skills |
|---|---|
| mattpocock/skills | diagnosing-bugs, tdd, codebase-design |
| affaan-m/ECC | api-design, backend-patterns, nestjs-patterns, prisma-patterns, postgres-patterns, redis-patterns, mcp-server-patterns, nodejs-keccak256 |

### python

Python: idioms, pytest, Django, data, and ML workflows.

Deploy project scope:

```cmd
.\scripts\Deploy-SkillSet-Py.cmd --set python
```

Skills:

| Repo | Skills |
|---|---|
| mattpocock/skills | diagnosing-bugs, tdd, codebase-design |
| affaan-m/ECC | python-patterns, python-testing, django-patterns, django-tdd, django-verification, mle-workflow, pytorch-patterns |

### agent-ops

Agent operations: skill scouting, stocktake, quality, context, parallelism, and local knowledge management.

Deploy project scope:

```cmd
.\scripts\Deploy-SkillSet-Py.cmd --set agent-ops
```

Skills:

| Repo | Skills |
|---|---|
| mattpocock/skills | writing-great-skills, handoff, grill-with-docs |
| affaan-m/ECC | skill-scout, skill-stocktake, skill-comply, knowledge-ops, parallel-execution-optimizer, strategic-compact, iterative-retrieval, workspace-surface-audit |

## 部署指令 / Deployment Commands

Windows 上建議使用 `scripts\Deploy-SkillSet-Py.cmd` 呼叫 Python deployer。它支援互動選擇、明確指定 `--target`、curated sets、單一或多個 skills，以及 dry run。

```cmd
# Preview only
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --dry-run

# Install a curated set into this workspace
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup

# Install for every supported agent surface, not just OpenCode
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --agent *

# Install a curated set globally
.\scripts\Deploy-SkillSet-Py.cmd --set core-dev --scope global

# Regenerate this catalog from local mirrors
.\scripts\Deploy-SkillSet.cmd -UpdateCatalog -DryRun

# Deploy individual skills
.\scripts\Deploy-SkillSet-Py.cmd --skill matt:handoff --skill ecc:terminal-ops --skill pony:ponytail-review
```

## CC Switch Note

CC Switch 可以分開評估。它比較像環境／模型／設定切換器，而不是此 skill catalog 的替代品。先完成本機 skill mirror 與部署腳本，再把 CC Switch 加進 `env-setup` 工作流或獨立的環境切換任務。

## 已知問題：`reasoning part 0 not found`

這通常是 session viewer／gateway／模型 fallback 的中繼資料解析問題：呼叫端嘗試讀取 `reasoning[0]`，但模型回應沒有該段落。如果 CLI 指令完成且檔案有產出，通常不會阻擋 skill mirroring 或 deployment。若要除錯，請檢查 model names、fallback providers、OpenCode session viewer，以及 gateway 是否支援 reasoning parts。

## Full Local Skill Catalog

| Repo | Skill | Purpose | Local file |
|---|---|---|---|
| mattpocock/skills | `ask-matt` | Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo. | `vendor\skill-sources\mattpocock-skills\skills\engineering\ask-matt\SKILL.md` |
| mattpocock/skills | `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary. | `vendor\skill-sources\mattpocock-skills\skills\engineering\codebase-design\SKILL.md` |
| mattpocock/skills | `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. | `vendor\skill-sources\mattpocock-skills\skills\engineering\diagnosing-bugs\SKILL.md` |
| mattpocock/skills | `domain-modeling` | Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model. | `vendor\skill-sources\mattpocock-skills\skills\engineering\domain-modeling\SKILL.md` |
| mattpocock/skills | `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code. | `vendor\skill-sources\mattpocock-skills\skills\misc\git-guardrails-claude-code\SKILL.md` |
| mattpocock/skills | `grilling` | Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases. | `vendor\skill-sources\mattpocock-skills\skills\productivity\grilling\SKILL.md` |
| mattpocock/skills | `grill-me` | A relentless interview to sharpen a plan or design. | `vendor\skill-sources\mattpocock-skills\skills\productivity\grill-me\SKILL.md` |
| mattpocock/skills | `grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. | `vendor\skill-sources\mattpocock-skills\skills\engineering\grill-with-docs\SKILL.md` |
| mattpocock/skills | `handoff` | Compact the current conversation into a handoff document for another agent to pick up. | `vendor\skill-sources\mattpocock-skills\skills\productivity\handoff\SKILL.md` |
| mattpocock/skills | `implement` | Implement a piece of work based on a PRD or set of issues. | `vendor\skill-sources\mattpocock-skills\skills\engineering\implement\SKILL.md` |
| mattpocock/skills | `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. | `vendor\skill-sources\mattpocock-skills\skills\engineering\improve-codebase-architecture\SKILL.md` |
| mattpocock/skills | `migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data. | `vendor\skill-sources\mattpocock-skills\skills\misc\migrate-to-shoehorn\SKILL.md` |
| mattpocock/skills | `prototype` | Build a throwaway prototype to flesh out a design — a runnable terminal app for state/business-logic questions, or several radically different UI variations toggleable from one route. | `vendor\skill-sources\mattpocock-skills\skills\engineering\prototype\SKILL.md` |
| mattpocock/skills | `resolving-merge-conflicts` | Use when you need to resolve an in-progress git merge/rebase conflict. | `vendor\skill-sources\mattpocock-skills\skills\engineering\resolving-merge-conflicts\SKILL.md` |
| mattpocock/skills | `scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section. | `vendor\skill-sources\mattpocock-skills\skills\misc\scaffold-exercises\SKILL.md` |
| mattpocock/skills | `setup-matt-pocock-skills` | Configure this repo for the engineering skills — set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills. | `vendor\skill-sources\mattpocock-skills\skills\engineering\setup-matt-pocock-skills\SKILL.md` |
| mattpocock/skills | `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing. | `vendor\skill-sources\mattpocock-skills\skills\misc\setup-pre-commit\SKILL.md` |
| mattpocock/skills | `tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests. | `vendor\skill-sources\mattpocock-skills\skills\engineering\tdd\SKILL.md` |
| mattpocock/skills | `teach` | Teach the user a new skill or concept, within this workspace. | `vendor\skill-sources\mattpocock-skills\skills\productivity\teach\SKILL.md` |
| mattpocock/skills | `to-issues` | Break a plan, spec, or PRD into independently-grabbable issues on the project issue tracker using tracer-bullet vertical slices. | `vendor\skill-sources\mattpocock-skills\skills\engineering\to-issues\SKILL.md` |
| mattpocock/skills | `to-prd` | Turn the current conversation into a PRD and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed. | `vendor\skill-sources\mattpocock-skills\skills\engineering\to-prd\SKILL.md` |
| mattpocock/skills | `triage` | Move issues and external PRs through a state machine of triage roles — categorise, verify, grill if needed, and write agent-ready briefs. | `vendor\skill-sources\mattpocock-skills\skills\engineering\triage\SKILL.md` |
| mattpocock/skills | `writing-great-skills` | Reference for writing and editing skills well — the vocabulary and principles that make a skill predictable. | `vendor\skill-sources\mattpocock-skills\skills\productivity\writing-great-skills\SKILL.md` |
| affaan-m/ECC | `accessibility` | Design, implement, and audit inclusive digital products using WCAG 2.2 Level AA | `vendor\skill-sources\affaan-m-ecc\skills\accessibility\SKILL.md` |
| affaan-m/ECC | `agent-architecture-audit` | Full-stack diagnostic for agent and LLM applications. Audits the 12-layer agent stack for wrapper regression, memory pollution, tool discipline failures, hidden repair loops, and rendering corruption. Produces severity-ranked findings with code-first fixes. Essential for developers building agent applications, autonomous loops, or any LLM-powered feature. | `vendor\skill-sources\affaan-m-ecc\skills\agent-architecture-audit\SKILL.md` |
| affaan-m/ECC | `agent-eval` | Head-to-head comparison of coding agents (Claude Code, Aider, Codex, etc.) on custom tasks with pass rate, cost, time, and consistency metrics | `vendor\skill-sources\affaan-m-ecc\skills\agent-eval\SKILL.md` |
| affaan-m/ECC | `agent-harness-construction` | Design and optimize AI agent action spaces, tool definitions, and observation formatting for higher completion rates. | `vendor\skill-sources\affaan-m-ecc\skills\agent-harness-construction\SKILL.md` |
| affaan-m/ECC | `agentic-engineering` | Operate as an agentic engineer using eval-first execution, decomposition, and cost-aware model routing. | `vendor\skill-sources\affaan-m-ecc\skills\agentic-engineering\SKILL.md` |
| affaan-m/ECC | `agentic-os` | Build persistent multi-agent operating systems on Claude Code. Covers kernel architecture, specialist agents, slash commands, file-based memory, scheduled automation, and state management without external databases. | `vendor\skill-sources\affaan-m-ecc\skills\agentic-os\SKILL.md` |
| affaan-m/ECC | `agent-introspection-debugging` | Structured self-debugging workflow for AI agent failures using capture, diagnosis, contained recovery, and introspection reports. | `vendor\skill-sources\affaan-m-ecc\skills\agent-introspection-debugging\SKILL.md` |
| affaan-m/ECC | `agent-payment-x402` | Add x402 payment execution to AI agents with per-task budgets, spending controls, and non-custodial wallets. Supports Base through agentwallet-sdk and X Layer through OKX Payments / OKX Agent Payments Protocol. | `vendor\skill-sources\affaan-m-ecc\skills\agent-payment-x402\SKILL.md` |
| affaan-m/ECC | `agent-self-evaluation` | Use after completing any non-trivial task. The agent self-rates its output on 5 axes — accuracy, completeness, clarity, actionability, conciseness — with concrete evidence per criterion. Produces a structured 1-5 scorecard with specific improvement suggestions. | `vendor\skill-sources\affaan-m-ecc\skills\agent-self-evaluation\SKILL.md` |
| affaan-m/ECC | `agent-sort` | Build an evidence-backed ECC install plan for a specific repo by sorting skills, commands, rules, hooks, and extras into DAILY vs LIBRARY buckets using parallel repo-aware review passes. Use when ECC should be trimmed to what a project actually needs instead of loading the full bundle. | `vendor\skill-sources\affaan-m-ecc\skills\agent-sort\SKILL.md` |
| affaan-m/ECC | `ai-first-engineering` | Engineering operating model for teams where AI agents generate a large share of implementation output. | `vendor\skill-sources\affaan-m-ecc\skills\ai-first-engineering\SKILL.md` |
| affaan-m/ECC | `ai-regression-testing` | Regression testing strategies for AI-assisted development. Sandbox-mode API testing without database dependencies, automated bug-check workflows, and patterns to catch AI blind spots where the same model writes and reviews code. | `vendor\skill-sources\affaan-m-ecc\skills\ai-regression-testing\SKILL.md` |
| affaan-m/ECC | `android-clean-architecture` | Clean Architecture patterns for Android and Kotlin Multiplatform projects — module structure, dependency rules, UseCases, Repositories, and data layer patterns. | `vendor\skill-sources\affaan-m-ecc\skills\android-clean-architecture\SKILL.md` |
| affaan-m/ECC | `angular-developer` | Generates Angular code and provides architectural guidance. Trigger when creating projects, components, or services, or for best practices on reactivity (signals, linkedSignal, resource), forms, dependency injection, routing, SSR, accessibility (ARIA), animations, styling (component styles, Tailwind CSS), testing, or CLI tooling. | `vendor\skill-sources\affaan-m-ecc\skills\angular-developer\SKILL.md` |
| affaan-m/ECC | `api-connector-builder` | Build a new API connector or provider by matching the target repo's existing integration pattern exactly. Use when adding one more integration without inventing a second architecture. | `vendor\skill-sources\affaan-m-ecc\skills\api-connector-builder\SKILL.md` |
| affaan-m/ECC | `api-design` | REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs. | `vendor\skill-sources\affaan-m-ecc\skills\api-design\SKILL.md` |
| affaan-m/ECC | `architecture-decision-records` | Capture architectural decisions made during Claude Code sessions as structured ADRs. Auto-detects decision moments, records context, alternatives considered, and rationale. Maintains an ADR log so future developers understand why the codebase is shaped the way it is. | `vendor\skill-sources\affaan-m-ecc\skills\architecture-decision-records\SKILL.md` |
| affaan-m/ECC | `article-writing` | Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form content in a distinctive voice derived from supplied examples or brand guidance. Use when the user wants polished written content longer than a paragraph, especially when voice consistency, structure, and credibility matter. | `vendor\skill-sources\affaan-m-ecc\skills\article-writing\SKILL.md` |
| affaan-m/ECC | `automation-audit-ops` | Evidence-first automation inventory and overlap audit workflow for ECC. Use when the user wants to know which jobs, hooks, connectors, MCP servers, or wrappers are live, broken, redundant, or missing before fixing anything. | `vendor\skill-sources\affaan-m-ecc\skills\automation-audit-ops\SKILL.md` |
| affaan-m/ECC | `autonomous-agent-harness` | Transform Claude Code into a fully autonomous agent system with persistent memory, scheduled operations, computer use, and task queuing. Replaces standalone agent frameworks (Hermes, AutoGPT) by leveraging Claude Code's native crons, dispatch, MCP tools, and memory. Use when the user wants continuous autonomous operation, scheduled tasks, or a self-directing agent loop. | `vendor\skill-sources\affaan-m-ecc\skills\autonomous-agent-harness\SKILL.md` |
| affaan-m/ECC | `autonomous-loops` | Patterns and architectures for autonomous Claude Code loops — from simple sequential pipelines to RFC-driven multi-agent DAG systems. | `vendor\skill-sources\affaan-m-ecc\skills\autonomous-loops\SKILL.md` |
| affaan-m/ECC | `backend-patterns` | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. | `vendor\skill-sources\affaan-m-ecc\skills\backend-patterns\SKILL.md` |
| affaan-m/ECC | `benchmark` | Use this skill to measure performance baselines, detect regressions before/after PRs, and compare stack alternatives. | `vendor\skill-sources\affaan-m-ecc\skills\benchmark\SKILL.md` |
| affaan-m/ECC | `benchmark-methodology` | >- | `vendor\skill-sources\affaan-m-ecc\skills\benchmark-methodology\SKILL.md` |
| affaan-m/ECC | `benchmark-optimization-loop` | Use when the user asks to make something faster, try many variants, run recursive optimization, benchmark latency/throughput/cost, or choose the best implementation by repeated measured tests. | `vendor\skill-sources\affaan-m-ecc\skills\benchmark-optimization-loop\SKILL.md` |
| affaan-m/ECC | `blender-motion-state-inspection` | Use this skill when inspecting Blender characters, rigs, poses, animation retargeting, ground contact, facing direction, or model-vs-motion alignment where screenshots alone are not enough. | `vendor\skill-sources\affaan-m-ecc\skills\blender-motion-state-inspection\SKILL.md` |
| affaan-m/ECC | `blueprint` | >- | `vendor\skill-sources\affaan-m-ecc\skills\blueprint\SKILL.md` |
| affaan-m/ECC | `brand-discovery` | >- | `vendor\skill-sources\affaan-m-ecc\skills\brand-discovery\SKILL.md` |
| affaan-m/ECC | `brand-voice` | Build a source-derived writing style profile from real posts, essays, launch notes, docs, or site copy, then reuse that profile across content, outreach, and social workflows. Use when the user wants voice consistency without generic AI writing tropes. | `vendor\skill-sources\affaan-m-ecc\skills\brand-voice\SKILL.md` |
| affaan-m/ECC | `browser-qa` | Use this skill to automate visual testing and UI interaction verification using browser automation after deploying features. | `vendor\skill-sources\affaan-m-ecc\skills\browser-qa\SKILL.md` |
| affaan-m/ECC | `bun-runtime` | Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support. | `vendor\skill-sources\affaan-m-ecc\skills\bun-runtime\SKILL.md` |
| affaan-m/ECC | `canary-watch` | Use this skill to monitor and verify a deployed URL after releases — checks HTTP endpoints, SSE streams, static assets, console errors, and performance regressions after deploys, merges, or dependency upgrades. Smoke / canary / post-deploy verification. | `vendor\skill-sources\affaan-m-ecc\skills\canary-watch\SKILL.md` |
| affaan-m/ECC | `carrier-relationship-management` | > | `vendor\skill-sources\affaan-m-ecc\skills\carrier-relationship-management\SKILL.md` |
| affaan-m/ECC | `cisco-ios-patterns` | Cisco IOS and IOS-XE review patterns for show commands, config hierarchy, wildcard masks, ACL placement, interface hygiene, and safe change-window verification. | `vendor\skill-sources\affaan-m-ecc\skills\cisco-ios-patterns\SKILL.md` |
| affaan-m/ECC | `ck` | Persistent per-project memory for Claude Code. Auto-loads project context on session start, tracks sessions with git activity, and writes to native memory. Commands run deterministic Node.js scripts — behavior is consistent across model versions. | `vendor\skill-sources\affaan-m-ecc\skills\ck\SKILL.md` |
| affaan-m/ECC | `claude-devfleet` | Orchestrate multi-agent coding tasks via Claude DevFleet — plan projects, dispatch parallel agents in isolated worktrees, monitor progress, and read structured reports. | `vendor\skill-sources\affaan-m-ecc\skills\claude-devfleet\SKILL.md` |
| affaan-m/ECC | `clickhouse-io` | ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads. | `vendor\skill-sources\affaan-m-ecc\skills\clickhouse-io\SKILL.md` |
| affaan-m/ECC | `click-path-audit` | Trace every user-facing button/touchpoint through its full state change sequence to find bugs where functions individually work but cancel each other out, produce wrong final state, or leave the UI in an inconsistent state. Use when: systematic debugging found no bugs but users report broken buttons, or after any major refactor touching shared state stores. | `vendor\skill-sources\affaan-m-ecc\skills\click-path-audit\SKILL.md` |
| affaan-m/ECC | `codebase-onboarding` | Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a starter CLAUDE.md. Use when joining a new project or setting up Claude Code for the first time in a repo. | `vendor\skill-sources\affaan-m-ecc\skills\codebase-onboarding\SKILL.md` |
| affaan-m/ECC | `codehealth-mcp` | Real-time structural Code Health via CodeScene MCP — review before edits, verify score deltas after changes, gate commits and PRs. Use when reviewing code quality, refactoring, checking if AI changes degraded a file, or before commit/PR. | `vendor\skill-sources\affaan-m-ecc\skills\codehealth-mcp\SKILL.md` |
| affaan-m/ECC | `code-tour` | Create CodeTour `.tour` files — persona-targeted, step-by-step walkthroughs with real file and line anchors. Use for onboarding tours, architecture walkthroughs, PR tours, RCA tours, and structured "explain how this works" requests. | `vendor\skill-sources\affaan-m-ecc\skills\code-tour\SKILL.md` |
| affaan-m/ECC | `coding-standards` | Baseline cross-project coding conventions for naming, readability, immutability, and code-quality review. Use detailed frontend or backend skills for framework-specific patterns. | `vendor\skill-sources\affaan-m-ecc\skills\coding-standards\SKILL.md` |
| affaan-m/ECC | `competitive-platform-analysis` | >- | `vendor\skill-sources\affaan-m-ecc\skills\competitive-platform-analysis\SKILL.md` |
| affaan-m/ECC | `competitive-report-structure` | >- | `vendor\skill-sources\affaan-m-ecc\skills\competitive-report-structure\SKILL.md` |
| affaan-m/ECC | `compose-multiplatform-patterns` | Compose Multiplatform and Jetpack Compose patterns for KMP projects — state management, navigation, theming, performance, and platform-specific UI. | `vendor\skill-sources\affaan-m-ecc\skills\compose-multiplatform-patterns\SKILL.md` |
| affaan-m/ECC | `config-gc` | Garbage collection for your Claude Code configuration. Periodically scans ~/.claude (skills, memory, hooks, permissions, MCP servers, caches) for redundant, stale, orphaned, or low-value items, then walks the user through a confirm-each-deletion cleanup. Use when the user says "clean up my config", "config GC", "too many skills", "audit my setup", "my .claude is bloated", or asks for a periodic config review. | `vendor\skill-sources\affaan-m-ecc\skills\config-gc\SKILL.md` |
| affaan-m/ECC | `configure-ecc` | Interactive installer for Everything Claude Code — guides users through selecting and installing skills and rules to user-level or project-level directories, verifies paths, and optionally optimizes installed files. | `vendor\skill-sources\affaan-m-ecc\skills\configure-ecc\SKILL.md` |
| affaan-m/ECC | `connections-optimizer` | Reorganize the user's X and LinkedIn network with review-first pruning, add/follow recommendations, and channel-specific warm outreach drafted in the user's real voice. Use when the user wants to clean up following lists, grow toward current priorities, or rebalance a social graph around higher-signal relationships. | `vendor\skill-sources\affaan-m-ecc\skills\connections-optimizer\SKILL.md` |
| affaan-m/ECC | `content-engine` | Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters, and repurposed multi-platform campaigns. Use when the user wants social posts, threads, scripts, content calendars, or one source asset adapted cleanly across platforms. | `vendor\skill-sources\affaan-m-ecc\skills\content-engine\SKILL.md` |
| affaan-m/ECC | `content-hash-cache-pattern` | Cache expensive file processing results using SHA-256 content hashes — path-independent, auto-invalidating, with service layer separation. | `vendor\skill-sources\affaan-m-ecc\skills\content-hash-cache-pattern\SKILL.md` |
| affaan-m/ECC | `context-budget` | Audits Claude Code context window consumption across agents, skills, MCP servers, and rules. Identifies bloat, redundant components, and produces prioritized token-savings recommendations. | `vendor\skill-sources\affaan-m-ecc\skills\context-budget\SKILL.md` |
| affaan-m/ECC | `continuous-agent-loop` | Patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls. | `vendor\skill-sources\affaan-m-ecc\skills\continuous-agent-loop\SKILL.md` |
| affaan-m/ECC | `continuous-learning` | [DEPRECATED - use continuous-learning-v2] Legacy v1 stop-hook skill extractor. v2 is a strict superset with instinct-based, project-scoped, hook-reliable learning. Do not invoke v1; route continuous learning, session learning, and pattern extraction requests to continuous-learning-v2. | `vendor\skill-sources\affaan-m-ecc\skills\continuous-learning\SKILL.md` |
| affaan-m/ECC | `continuous-learning-v2` | Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into skills/commands/agents. v2.1 adds project-scoped instincts to prevent cross-project contamination. | `vendor\skill-sources\affaan-m-ecc\skills\continuous-learning-v2\SKILL.md` |
| affaan-m/ECC | `cost-aware-llm-pipeline` | Cost optimization patterns for LLM API usage — model routing by task complexity, budget tracking, retry logic, and prompt caching. | `vendor\skill-sources\affaan-m-ecc\skills\cost-aware-llm-pipeline\SKILL.md` |
| affaan-m/ECC | `cost-tracking` | Track and report Claude Code token usage, spending, and budgets from a local cost-tracking database. Use when the user asks about costs, spending, usage, tokens, budgets, or cost breakdowns by project, tool, session, or date. | `vendor\skill-sources\affaan-m-ecc\skills\cost-tracking\SKILL.md` |
| affaan-m/ECC | `council` | Convene a four-voice council for ambiguous decisions, tradeoffs, and go/no-go calls. Use when multiple valid paths exist and you need structured disagreement before choosing. | `vendor\skill-sources\affaan-m-ecc\skills\council\SKILL.md` |
| affaan-m/ECC | `cpp-coding-standards` | C++ coding standards based on the C++ Core Guidelines (isocpp.github.io). Use when writing, reviewing, or refactoring C++ code to enforce modern, safe, and idiomatic practices. | `vendor\skill-sources\affaan-m-ecc\skills\cpp-coding-standards\SKILL.md` |
| affaan-m/ECC | `cpp-testing` | Use only when writing/updating/fixing C++ tests, configuring GoogleTest/CTest, diagnosing failing or flaky tests, or adding coverage/sanitizers. | `vendor\skill-sources\affaan-m-ecc\skills\cpp-testing\SKILL.md` |
| affaan-m/ECC | `crosspost` | Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. Adapts content per platform using content-engine patterns. Never posts identical content cross-platform. Use when the user wants to distribute content across social platforms. | `vendor\skill-sources\affaan-m-ecc\skills\crosspost\SKILL.md` |
| affaan-m/ECC | `csharp-testing` | C# and .NET testing patterns with xUnit, FluentAssertions, mocking, integration tests, and test organization best practices. | `vendor\skill-sources\affaan-m-ecc\skills\csharp-testing\SKILL.md` |
| affaan-m/ECC | `customer-billing-ops` | Operate customer billing workflows such as subscriptions, refunds, churn triage, billing-portal recovery, and plan analysis using connected billing tools like Stripe. Use when the user needs to help a customer, inspect subscription state, or manage revenue-impacting billing operations. | `vendor\skill-sources\affaan-m-ecc\skills\customer-billing-ops\SKILL.md` |
| affaan-m/ECC | `customs-trade-compliance` | > | `vendor\skill-sources\affaan-m-ecc\skills\customs-trade-compliance\SKILL.md` |
| affaan-m/ECC | `dart-flutter-patterns` | Production-ready Dart and Flutter patterns covering null safety, immutable state, async composition, widget architecture, popular state management frameworks (BLoC, Riverpod, Provider), GoRouter navigation, Dio networking, Freezed code generation, and clean architecture. | `vendor\skill-sources\affaan-m-ecc\skills\dart-flutter-patterns\SKILL.md` |
| affaan-m/ECC | `dashboard-builder` | Build monitoring dashboards that answer real operator questions for Grafana, SigNoz, and similar platforms. Use when turning metrics into a working dashboard instead of a vanity board. | `vendor\skill-sources\affaan-m-ecc\skills\dashboard-builder\SKILL.md` |
| affaan-m/ECC | `database-migrations` | Database migration best practices for schema changes, data migrations, rollbacks, and zero-downtime deployments across PostgreSQL, MySQL, and common ORMs (Prisma, Drizzle, Kysely, Django, TypeORM, golang-migrate). | `vendor\skill-sources\affaan-m-ecc\skills\database-migrations\SKILL.md` |
| affaan-m/ECC | `data-scraper-agent` | Build a fully automated AI-powered data collection agent for any public source — job boards, prices, news, GitHub, sports, anything. Scrapes on a schedule, enriches data with a free LLM (Gemini Flash), stores results in Notion/Sheets/Supabase, and learns from user feedback. Runs 100% free on GitHub Actions. Use when the user wants to monitor, collect, or track any public data automatically. | `vendor\skill-sources\affaan-m-ecc\skills\data-scraper-agent\SKILL.md` |
| affaan-m/ECC | `data-throughput-accelerator` | Use when large data ingestion, backfill, export, ETL, warehouse loading, manifest catch-up, or table synchronization needs to become much faster while preserving data correctness. | `vendor\skill-sources\affaan-m-ecc\skills\data-throughput-accelerator\SKILL.md` |
| affaan-m/ECC | `deep-research` | Multi-source deep research using firecrawl and exa MCPs. Searches the web, synthesizes findings, and delivers cited reports with source attribution. Use when the user wants thorough research on any topic with evidence and citations. | `vendor\skill-sources\affaan-m-ecc\skills\deep-research\SKILL.md` |
| affaan-m/ECC | `defi-amm-security` | Security checklist for Solidity AMM contracts, liquidity pools, and swap flows. Covers reentrancy, CEI ordering, donation or inflation attacks, oracle manipulation, slippage, admin controls, and integer math. | `vendor\skill-sources\affaan-m-ecc\skills\defi-amm-security\SKILL.md` |
| affaan-m/ECC | `deployment-patterns` | Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies, and production readiness checklists for web applications. | `vendor\skill-sources\affaan-m-ecc\skills\deployment-patterns\SKILL.md` |
| affaan-m/ECC | `design-system` | Use this skill to generate or audit design systems, check visual consistency, and review PRs that touch styling. | `vendor\skill-sources\affaan-m-ecc\skills\design-system\SKILL.md` |
| affaan-m/ECC | `django-celery` | Django + Celery async task patterns — configuration, task design, beat scheduling, retries, canvas workflows, monitoring, and testing. Use when adding background jobs, scheduled tasks, or async processing to a Django app. | `vendor\skill-sources\affaan-m-ecc\skills\django-celery\SKILL.md` |
| affaan-m/ECC | `django-patterns` | Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and production-grade Django apps. | `vendor\skill-sources\affaan-m-ecc\skills\django-patterns\SKILL.md` |
| affaan-m/ECC | `django-security` | Django security best practices, authentication, authorization, CSRF protection, SQL injection prevention, XSS prevention, and secure deployment configurations. | `vendor\skill-sources\affaan-m-ecc\skills\django-security\SKILL.md` |
| affaan-m/ECC | `django-tdd` | Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs. | `vendor\skill-sources\affaan-m-ecc\skills\django-tdd\SKILL.md` |
| affaan-m/ECC | `django-verification` | Verification loop for Django projects: migrations, linting, tests with coverage, security scans, and deployment readiness checks before release or PR. | `vendor\skill-sources\affaan-m-ecc\skills\django-verification\SKILL.md` |
| affaan-m/ECC | `dmux-workflows` | Multi-agent orchestration using dmux (tmux pane manager for AI agents). Patterns for parallel agent workflows across Claude Code, Codex, OpenCode, and other harnesses. Use when running multiple agent sessions in parallel or coordinating multi-agent development workflows. | `vendor\skill-sources\affaan-m-ecc\skills\dmux-workflows\SKILL.md` |
| affaan-m/ECC | `docker-patterns` | Docker and Docker Compose patterns for local development, container security, networking, volume strategies, and multi-service orchestration. | `vendor\skill-sources\affaan-m-ecc\skills\docker-patterns\SKILL.md` |
| affaan-m/ECC | `documentation-lookup` | Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code examples, or when the user names a framework (e.g. React, Next.js, Prisma). | `vendor\skill-sources\affaan-m-ecc\skills\documentation-lookup\SKILL.md` |
| affaan-m/ECC | `dotnet-patterns` | Idiomatic C# and .NET patterns, conventions, dependency injection, async/await, and best practices for building robust, maintainable .NET applications. | `vendor\skill-sources\affaan-m-ecc\skills\dotnet-patterns\SKILL.md` |
| affaan-m/ECC | `dynamic-workflow-mode` | Design task-local harnesses, eval gates, and reusable skill extraction for Claude dynamic workflow mode and other adaptive agent harnesses. | `vendor\skill-sources\affaan-m-ecc\skills\dynamic-workflow-mode\SKILL.md` |
| affaan-m/ECC | `e2e-testing` | Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies. | `vendor\skill-sources\affaan-m-ecc\skills\e2e-testing\SKILL.md` |
| affaan-m/ECC | `ecc-guide` | Guide users through ECC's current agents, skills, commands, hooks, rules, install profiles, and project onboarding by reading the live repository surface before answering. | `vendor\skill-sources\affaan-m-ecc\skills\ecc-guide\SKILL.md` |
| affaan-m/ECC | `ecc-tools-cost-audit` | Evidence-first ECC Tools burn and billing audit workflow. Use when investigating runaway PR creation, quota bypass, premium-model leakage, duplicate jobs, or GitHub App cost spikes in the ECC Tools repo. | `vendor\skill-sources\affaan-m-ecc\skills\ecc-tools-cost-audit\SKILL.md` |
| affaan-m/ECC | `email-ops` | Evidence-first mailbox triage, drafting, send verification, and sent-mail-safe follow-up workflow for ECC. Use when the user wants to organize email, draft or send through the real mail surface, or prove what landed in Sent. | `vendor\skill-sources\affaan-m-ecc\skills\email-ops\SKILL.md` |
| affaan-m/ECC | `energy-procurement` | > | `vendor\skill-sources\affaan-m-ecc\skills\energy-procurement\SKILL.md` |
| affaan-m/ECC | `enterprise-agent-ops` | Operate long-lived agent workloads with observability, security boundaries, and lifecycle management. | `vendor\skill-sources\affaan-m-ecc\skills\enterprise-agent-ops\SKILL.md` |
| affaan-m/ECC | `error-handling` | Patterns for robust error handling across TypeScript, Python, and Go. Covers typed errors, error boundaries, retries, circuit breakers, and user-facing error messages. | `vendor\skill-sources\affaan-m-ecc\skills\error-handling\SKILL.md` |
| affaan-m/ECC | `eval-harness` | Formal evaluation framework for Claude Code sessions implementing eval-driven development (EDD) principles | `vendor\skill-sources\affaan-m-ecc\skills\eval-harness\SKILL.md` |
| affaan-m/ECC | `evm-token-decimals` | Prevent silent decimal mismatch bugs across EVM chains. Covers runtime decimal lookup, chain-aware caching, bridged-token precision drift, and safe normalization for bots, dashboards, and DeFi tools. | `vendor\skill-sources\affaan-m-ecc\skills\evm-token-decimals\SKILL.md` |
| affaan-m/ECC | `exa-search` | Neural search via Exa MCP for web, code, and company research. Use when the user needs web search, code examples, company intel, people lookup, or AI-powered deep research with Exa's neural search engine. | `vendor\skill-sources\affaan-m-ecc\skills\exa-search\SKILL.md` |
| affaan-m/ECC | `fal-ai-media` | Unified media generation via fal.ai MCP — image, video, and audio. Covers text-to-image (Nano Banana), text/image-to-video (Seedance, Kling, Veo 3), text-to-speech (CSM-1B), and video-to-audio (ThinkSound). Use when the user wants to generate images, videos, or audio with AI. | `vendor\skill-sources\affaan-m-ecc\skills\fal-ai-media\SKILL.md` |
| affaan-m/ECC | `fastapi-patterns` | FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injection, async handlers, authentication, authorization, transactional service layers, and testing with httpx and pytest. | `vendor\skill-sources\affaan-m-ecc\skills\fastapi-patterns\SKILL.md` |
| affaan-m/ECC | `finance-billing-ops` | Evidence-first revenue, pricing, refunds, team-billing, and billing-model truth workflow for ECC. Use when the user wants a sales snapshot, pricing comparison, duplicate-charge diagnosis, or code-backed billing reality instead of generic payments advice. | `vendor\skill-sources\affaan-m-ecc\skills\finance-billing-ops\SKILL.md` |
| affaan-m/ECC | `flox-environments` | Create reproducible, cross-platform (macOS/Linux) development environments with Flox, a declarative Nix-based environment manager. Use when setting up project toolchains for any language, installing system-level dependencies (compilers, databases, native libs like openssl/BLAS), pinning exact package versions for a team, running local services (PostgreSQL, Redis, Kafka), onboarding developers with one command, or solving 'works on my machine' problems — including agent/vibe-coding setups that need project-scoped tools without sudo. Also use when the user mentions .flox/, manifest.toml, flox activate, or FloxHub. | `vendor\skill-sources\affaan-m-ecc\skills\flox-environments\SKILL.md` |
| affaan-m/ECC | `flutter-dart-code-review` | Library-agnostic Flutter/Dart code review checklist covering widget best practices, state management patterns (BLoC, Riverpod, Provider, GetX, MobX, Signals), Dart idioms, performance, accessibility, security, and clean architecture. | `vendor\skill-sources\affaan-m-ecc\skills\flutter-dart-code-review\SKILL.md` |
| affaan-m/ECC | `foundation-models-on-device` | Apple FoundationModels framework for on-device LLM — text generation, guided generation with @Generable, tool calling, and snapshot streaming in iOS 26+. | `vendor\skill-sources\affaan-m-ecc\skills\foundation-models-on-device\SKILL.md` |
| affaan-m/ECC | `frontend-a11y` | > | `vendor\skill-sources\affaan-m-ecc\skills\frontend-a11y\SKILL.md` |
| affaan-m/ECC | `frontend-design-direction` | Set an ECC-specific frontend design direction for production UI work. Use when building or improving websites, dashboards, applications, components, landing pages, visual tools, or any web UI that needs stronger product-specific design judgment. | `vendor\skill-sources\affaan-m-ecc\skills\frontend-design-direction\SKILL.md` |
| affaan-m/ECC | `frontend-patterns` | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. | `vendor\skill-sources\affaan-m-ecc\skills\frontend-patterns\SKILL.md` |
| affaan-m/ECC | `frontend-slides` | Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices. | `vendor\skill-sources\affaan-m-ecc\skills\frontend-slides\SKILL.md` |
| affaan-m/ECC | `fsharp-testing` | F# testing patterns with xUnit, FsUnit, Unquote, FsCheck property-based testing, integration tests, and test organization best practices. | `vendor\skill-sources\affaan-m-ecc\skills\fsharp-testing\SKILL.md` |
| affaan-m/ECC | `gan-style-harness` | GAN-inspired Generator-Evaluator agent harness for building high-quality applications autonomously. Based on Anthropic's March 2026 harness design paper. | `vendor\skill-sources\affaan-m-ecc\skills\gan-style-harness\SKILL.md` |
| affaan-m/ECC | `gateguard` | Fact-forcing gate that blocks Edit/Write/Bash (including MultiEdit) and demands concrete investigation (importers, data schemas, user instruction) before allowing the action. Measurably improves output quality by +2.25 points vs ungated agents. | `vendor\skill-sources\affaan-m-ecc\skills\gateguard\SKILL.md` |
| affaan-m/ECC | `generating-python-installer` | Commercial-grade Python installer expert for Windows: Nuitka extreme compilation, dist slimming, DLL footprint analysis, and Inno Setup packaging to ship the smallest, fastest installers. Use only for advanced packaging/optimization (minimal size, fast startup), not basic script-to-exe conversion. 中文触发：Nuitka 极限优化、Python 商业打包、极限编译 Python、dist 瘦身、DLL 分析、最小安装包、最快启动、商业级打包风格 | `vendor\skill-sources\affaan-m-ecc\skills\generating-python-installer\SKILL.md` |
| affaan-m/ECC | `github-ops` | GitHub repository operations, automation, and management. Issue triage, PR management, CI/CD operations, release management, and security monitoring using the gh CLI. Use when the user wants to manage GitHub issues, PRs, CI status, releases, contributors, stale items, or any GitHub operational task beyond simple git commands. | `vendor\skill-sources\affaan-m-ecc\skills\github-ops\SKILL.md` |
| affaan-m/ECC | `git-workflow` | Git workflow patterns including branching strategies, commit conventions, merge vs rebase, conflict resolution, and collaborative development best practices for teams of all sizes. | `vendor\skill-sources\affaan-m-ecc\skills\git-workflow\SKILL.md` |
| affaan-m/ECC | `golang-patterns` | Idiomatic Go patterns, best practices, and conventions for building robust, efficient, and maintainable Go applications. | `vendor\skill-sources\affaan-m-ecc\skills\golang-patterns\SKILL.md` |
| affaan-m/ECC | `golang-testing` | Go testing patterns including table-driven tests, subtests, benchmarks, fuzzing, and test coverage. Follows TDD methodology with idiomatic Go practices. | `vendor\skill-sources\affaan-m-ecc\skills\golang-testing\SKILL.md` |
| affaan-m/ECC | `google-workspace-ops` | Operate across Google Drive, Docs, Sheets, and Slides as one workflow surface for plans, trackers, decks, and shared documents. Use when the user needs to find, summarize, edit, migrate, or clean up Google Workspace assets without dropping to raw tool calls. | `vendor\skill-sources\affaan-m-ecc\skills\google-workspace-ops\SKILL.md` |
| affaan-m/ECC | `healthcare-cdss-patterns` | Clinical Decision Support System (CDSS) development patterns. Drug interaction checking, dose validation, clinical scoring (NEWS2, qSOFA), alert severity classification, and integration into EMR workflows. | `vendor\skill-sources\affaan-m-ecc\skills\healthcare-cdss-patterns\SKILL.md` |
| affaan-m/ECC | `healthcare-emr-patterns` | EMR/EHR development patterns for healthcare applications. Clinical safety, encounter workflows, prescription generation, clinical decision support integration, and accessibility-first UI for medical data entry. | `vendor\skill-sources\affaan-m-ecc\skills\healthcare-emr-patterns\SKILL.md` |
| affaan-m/ECC | `healthcare-eval-harness` | Patient safety evaluation harness for healthcare application deployments. Automated test suites for CDSS accuracy, PHI exposure, clinical workflow integrity, and integration compliance. Blocks deployments on safety failures. | `vendor\skill-sources\affaan-m-ecc\skills\healthcare-eval-harness\SKILL.md` |
| affaan-m/ECC | `healthcare-phi-compliance` | Protected Health Information (PHI) and Personally Identifiable Information (PII) compliance patterns for healthcare applications. Covers data classification, access control, audit trails, encryption, and common leak vectors. | `vendor\skill-sources\affaan-m-ecc\skills\healthcare-phi-compliance\SKILL.md` |
| affaan-m/ECC | `hermes-imports` | Convert local Hermes operator workflows into sanitized ECC skills and release-pack artifacts. Use when preparing a Hermes workflow for public ECC reuse without leaking private workspace state, credentials, or local-only paths. | `vendor\skill-sources\affaan-m-ecc\skills\hermes-imports\SKILL.md` |
| affaan-m/ECC | `hexagonal-architecture` | Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dependency inversion, and testable use-case orchestration across TypeScript, Java, Kotlin, and Go services. | `vendor\skill-sources\affaan-m-ecc\skills\hexagonal-architecture\SKILL.md` |
| affaan-m/ECC | `hipaa-compliance` | HIPAA-specific entrypoint for healthcare privacy and security work. Use when a task is explicitly framed around HIPAA, PHI handling, covered entities, BAAs, breach posture, or US healthcare compliance requirements. | `vendor\skill-sources\affaan-m-ecc\skills\hipaa-compliance\SKILL.md` |
| affaan-m/ECC | `homelab-network-readiness` | Readiness checklist for homelab VLAN segmentation, local DNS filtering, and WireGuard-style remote access before changing router, firewall, DHCP, or VPN configuration. | `vendor\skill-sources\affaan-m-ecc\skills\homelab-network-readiness\SKILL.md` |
| affaan-m/ECC | `homelab-network-setup` | Practical home and homelab network planning for gateways, switches, access points, IP ranges, DHCP reservations, DNS, cabling, and common beginner mistakes. | `vendor\skill-sources\affaan-m-ecc\skills\homelab-network-setup\SKILL.md` |
| affaan-m/ECC | `homelab-pihole-dns` | Pi-hole installation, blocklist management, DNS-over-HTTPS setup, DHCP integration, local DNS records, and troubleshooting broken DNS resolution on a home network. | `vendor\skill-sources\affaan-m-ecc\skills\homelab-pihole-dns\SKILL.md` |
| affaan-m/ECC | `homelab-vlan-segmentation` | Segmenting home networks into VLANs for IoT, guest, trusted, and server traffic using UniFi, pfSense/OPNsense, and MikroTik — including switch trunk config, firewall rules, and wireless SSID mapping. | `vendor\skill-sources\affaan-m-ecc\skills\homelab-vlan-segmentation\SKILL.md` |
| affaan-m/ECC | `homelab-wireguard-vpn` | WireGuard VPN server setup, peer configuration, key generation, split tunneling vs full tunnel routing, and remote access to a home network from mobile and laptop clients. | `vendor\skill-sources\affaan-m-ecc\skills\homelab-wireguard-vpn\SKILL.md` |
| affaan-m/ECC | `hookify-rules` | This skill should be used when the user asks to create a hookify rule, write a hook rule, configure hookify, add a hookify rule, or needs guidance on hookify rule syntax and patterns. | `vendor\skill-sources\affaan-m-ecc\skills\hookify-rules\SKILL.md` |
| affaan-m/ECC | `inherit-legacy-style` | Legacy-project style inheritance skill. Use when the user types /inherit-legacy-style, or when onboarding an AI coding agent onto a hand-written legacy project and you need to prevent "style drift" (the model imposing its pretrained mainstream idioms onto the project). Language- and framework-agnostic — it aligns meta-architecture only, not syntax. Once run, it becomes a behavioral constraint on all subsequent coding tasks. Do NOT use for pure research or one-off questions unrelated to code-style alignment. | `vendor\skill-sources\affaan-m-ecc\skills\inherit-legacy-style\SKILL.md` |
| affaan-m/ECC | `intent-driven-development` | Turn ambiguous or high-impact product and engineering changes into scoped, verifiable acceptance criteria before or alongside implementation. Use when a user asks to clarify a feature, define acceptance criteria, de-risk a security/data/migration/integration change, prepare implementation requirements for another agent, or make a complex request testable. Do not trigger for trivial edits, straightforward fixes, active debugging, code review, or implementation requests whose acceptance conditions are already clear unless the user explicitly invokes this skill. | `vendor\skill-sources\affaan-m-ecc\skills\intent-driven-development\SKILL.md` |
| affaan-m/ECC | `inventory-demand-planning` | > | `vendor\skill-sources\affaan-m-ecc\skills\inventory-demand-planning\SKILL.md` |
| affaan-m/ECC | `investor-materials` | Create and update pitch decks, one-pagers, investor memos, accelerator applications, financial models, and fundraising materials. Use when the user needs investor-facing documents, projections, use-of-funds tables, milestone plans, or materials that must stay internally consistent across multiple fundraising assets. | `vendor\skill-sources\affaan-m-ecc\skills\investor-materials\SKILL.md` |
| affaan-m/ECC | `investor-outreach` | Draft cold emails, warm intro blurbs, follow-ups, update emails, and investor communications for fundraising. Use when the user wants outreach to angels, VCs, strategic investors, or accelerators and needs concise, personalized, investor-facing messaging. | `vendor\skill-sources\affaan-m-ecc\skills\investor-outreach\SKILL.md` |
| affaan-m/ECC | `ios-icon-gen` | Generate iOS app icons as PNG imagesets for Xcode asset catalogs from SF Symbols (5000+ Apple-native) or Iconify API (275k+ open source icons from 200+ collections). Use when generating icons, creating icon assets, adding icons to asset catalog, or searching for icons for iOS projects. | `vendor\skill-sources\affaan-m-ecc\skills\ios-icon-gen\SKILL.md` |
| affaan-m/ECC | `iterative-retrieval` | Pattern for progressively refining context retrieval to solve the subagent context problem | `vendor\skill-sources\affaan-m-ecc\skills\iterative-retrieval\SKILL.md` |
| affaan-m/ECC | `ito-basket-compare` | Compare Itô prediction-market baskets against a user's knowledge base, portfolio notes, financial context, watchlist, or research thesis. Use for read-only basket comparison and gap analysis without investment advice or live trading. | `vendor\skill-sources\affaan-m-ecc\skills\ito-basket-compare\SKILL.md` |
| affaan-m/ECC | `ito-data-atlas-agent` | Design background Data Atlas style agents for Itô basket research, market discovery, parameter drafting, and human-in-the-loop editing. Use for architecture and workflow planning, not live order execution. | `vendor\skill-sources\affaan-m-ecc\skills\ito-data-atlas-agent\SKILL.md` |
| affaan-m/ECC | `ito-market-intelligence` | Research prediction-market events, venues, underliers, liquidity, and news context for Itô basket workflows. Use for read-only market intelligence, API-gated Itô exploration, and source-grounded prediction-market briefings without investment advice or live trading. | `vendor\skill-sources\affaan-m-ecc\skills\ito-market-intelligence\SKILL.md` |
| affaan-m/ECC | `ito-trade-planner` | Build a non-advisory prediction-market trade planning worksheet for Itô or venue workflows. Use to inspect venues, underliers, constraints, order prerequisites, and manual execution steps without placing trades or recommending positions. | `vendor\skill-sources\affaan-m-ecc\skills\ito-trade-planner\SKILL.md` |
| affaan-m/ECC | `java-coding-standards` | Java coding standards for Spring Boot and Quarkus services: naming, immutability, Optional usage, streams, exceptions, generics, CDI, reactive patterns, and project layout. Automatically applies framework-specific conventions. | `vendor\skill-sources\affaan-m-ecc\skills\java-coding-standards\SKILL.md` |
| affaan-m/ECC | `jira-integration` | Use this skill when retrieving Jira tickets, analyzing requirements, updating ticket status, adding comments, or transitioning issues. Provides Jira API patterns via MCP or direct REST calls. | `vendor\skill-sources\affaan-m-ecc\skills\jira-integration\SKILL.md` |
| affaan-m/ECC | `jpa-patterns` | JPA/Hibernate patterns for entity design, relationships, query optimization, transactions, auditing, indexing, pagination, and pooling in Spring Boot. | `vendor\skill-sources\affaan-m-ecc\skills\jpa-patterns\SKILL.md` |
| affaan-m/ECC | `knowledge-ops` | Knowledge base management, ingestion, sync, and retrieval across multiple storage layers (local files, MCP memory, vector stores, Git repos). Use when the user wants to save, organize, sync, deduplicate, or search across their knowledge systems. | `vendor\skill-sources\affaan-m-ecc\skills\knowledge-ops\SKILL.md` |
| affaan-m/ECC | `kotlin-coroutines-flows` | Kotlin Coroutines and Flow patterns for Android and KMP — structured concurrency, Flow operators, StateFlow, error handling, and testing. | `vendor\skill-sources\affaan-m-ecc\skills\kotlin-coroutines-flows\SKILL.md` |
| affaan-m/ECC | `kotlin-exposed-patterns` | JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repository pattern. | `vendor\skill-sources\affaan-m-ecc\skills\kotlin-exposed-patterns\SKILL.md` |
| affaan-m/ECC | `kotlin-ktor-patterns` | Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication testing. | `vendor\skill-sources\affaan-m-ecc\skills\kotlin-ktor-patterns\SKILL.md` |
| affaan-m/ECC | `kotlin-patterns` | Idiomatic Kotlin patterns, best practices, and conventions for building robust, efficient, and maintainable Kotlin applications with coroutines, null safety, and DSL builders. | `vendor\skill-sources\affaan-m-ecc\skills\kotlin-patterns\SKILL.md` |
| affaan-m/ECC | `kotlin-testing` | Kotlin testing patterns with Kotest, MockK, coroutine testing, property-based testing, and Kover coverage. Follows TDD methodology with idiomatic Kotlin practices. | `vendor\skill-sources\affaan-m-ecc\skills\kotlin-testing\SKILL.md` |
| affaan-m/ECC | `kubernetes-patterns` | Kubernetes workload patterns, resource management, RBAC, probes, autoscaling, ConfigMap/Secret handling, and kubectl debugging for production-grade deployments. | `vendor\skill-sources\affaan-m-ecc\skills\kubernetes-patterns\SKILL.md` |
| affaan-m/ECC | `laravel-patterns` | Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and API resources for production apps. | `vendor\skill-sources\affaan-m-ecc\skills\laravel-patterns\SKILL.md` |
| affaan-m/ECC | `laravel-plugin-discovery` | Discover and evaluate Laravel packages via LaraPlugins.io MCP. Use when the user wants to find plugins, check package health, or assess Laravel/PHP compatibility. | `vendor\skill-sources\affaan-m-ecc\skills\laravel-plugin-discovery\SKILL.md` |
| affaan-m/ECC | `laravel-security` | Laravel security best practices — authentication, authorization, Eloquent safety, CSRF, XSS prevention, API security, and secure deployment configurations. | `vendor\skill-sources\affaan-m-ecc\skills\laravel-security\SKILL.md` |
| affaan-m/ECC | `laravel-tdd` | Laravel testing strategies with PHPUnit, Pest, model factories, HTTP tests, Sanctum authentication testing, mocking, and coverage. | `vendor\skill-sources\affaan-m-ecc\skills\laravel-tdd\SKILL.md` |
| affaan-m/ECC | `laravel-verification` | Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security scans, and deployment readiness. | `vendor\skill-sources\affaan-m-ecc\skills\laravel-verification\SKILL.md` |
| affaan-m/ECC | `latency-critical-systems` | Use for latency-sensitive systems such as realtime dashboards, market data, streaming agents, execution gateways, queues, caches, or HFT-like infrastructure where freshness and p95 latency matter. | `vendor\skill-sources\affaan-m-ecc\skills\latency-critical-systems\SKILL.md` |
| affaan-m/ECC | `lead-intelligence` | AI-native lead intelligence and outreach pipeline. Replaces Apollo, Clay, and ZoomInfo with agent-powered signal scoring, mutual ranking, warm path discovery, source-derived voice modeling, and channel-specific outreach across email, LinkedIn, and X. Use when the user wants to find, qualify, and reach high-value contacts. | `vendor\skill-sources\affaan-m-ecc\skills\lead-intelligence\SKILL.md` |
| affaan-m/ECC | `liquid-glass-design` | iOS 26 Liquid Glass design system — dynamic glass material with blur, reflection, and interactive morphing for SwiftUI, UIKit, and WidgetKit. | `vendor\skill-sources\affaan-m-ecc\skills\liquid-glass-design\SKILL.md` |
| affaan-m/ECC | `llm-trading-agent-security` | Security patterns for autonomous trading agents with wallet or transaction authority. Covers prompt injection, spend limits, pre-send simulation, circuit breakers, MEV protection, and key handling. | `vendor\skill-sources\affaan-m-ecc\skills\llm-trading-agent-security\SKILL.md` |
| affaan-m/ECC | `logistics-exception-management` | > | `vendor\skill-sources\affaan-m-ecc\skills\logistics-exception-management\SKILL.md` |
| affaan-m/ECC | `make-interfaces-feel-better` | Apply concrete design-engineering details that make interfaces feel polished. Use when reviewing or improving UI spacing, typography, borders, shadows, motion, hit areas, icons, text wrapping, and interaction states. | `vendor\skill-sources\affaan-m-ecc\skills\make-interfaces-feel-better\SKILL.md` |
| affaan-m/ECC | `manim-video` | Build reusable Manim explainers for technical concepts, graphs, system diagrams, and product walkthroughs, then hand off to the wider ECC video stack if needed. Use when the user wants a clean animated explainer rather than a generic talking-head script. | `vendor\skill-sources\affaan-m-ecc\skills\manim-video\SKILL.md` |
| affaan-m/ECC | `marketing-campaign` | End-to-end marketing campaign planning and execution. Covers audience research, positioning, campaign angle definition, landing page copy, email sequences, social posts, ad copy, short-form video scripts, and content calendars. Use as the orchestration layer for multi-channel product launches. | `vendor\skill-sources\affaan-m-ecc\skills\marketing-campaign\SKILL.md` |
| affaan-m/ECC | `market-research` | Conduct market research, competitive analysis, investor due diligence, and industry intelligence with source attribution and decision-oriented summaries. Use when the user wants market sizing, competitor comparisons, fund research, technology scans, or research that informs business decisions. | `vendor\skill-sources\affaan-m-ecc\skills\market-research\SKILL.md` |
| affaan-m/ECC | `mcp-server-patterns` | Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or official MCP docs for latest API. | `vendor\skill-sources\affaan-m-ecc\skills\mcp-server-patterns\SKILL.md` |
| affaan-m/ECC | `messages-ops` | Evidence-first live messaging workflow for ECC. Use when the user wants to read texts or DMs, recover a recent one-time code, inspect a thread before replying, or prove which message source was actually checked. | `vendor\skill-sources\affaan-m-ecc\skills\messages-ops\SKILL.md` |
| affaan-m/ECC | `ml-adoption-playbook` | End-to-end methodology for AI agents and software engineers to add machine learning algorithms to existing non-ML codebases. Covers problem framing, data readiness, architectural decoupling, and baseline model integration. | `vendor\skill-sources\affaan-m-ecc\skills\ml-adoption-playbook\SKILL.md` |
| affaan-m/ECC | `mle-workflow` | Production machine-learning engineering workflow for data contracts, reproducible training, model evaluation, deployment, monitoring, and rollback. Use when building, reviewing, or hardening ML systems beyond one-off notebooks. | `vendor\skill-sources\affaan-m-ecc\skills\mle-workflow\SKILL.md` |
| affaan-m/ECC | `motion-advanced` | Advanced motion patterns for React / Next.js — drag & drop, gestures, text animations, SVG path drawing, custom hooks, imperative sequences (useAnimate), loaders, and the full API decision tree. Requires motion-foundations. | `vendor\skill-sources\affaan-m-ecc\skills\motion-advanced\SKILL.md` |
| affaan-m/ECC | `motion-foundations` | Motion tokens, spring presets, performance rules, device adaptation, accessibility enforcement, and SSR safety for React / Next.js using motion/react. Foundation layer — all other motion skills depend on this. | `vendor\skill-sources\affaan-m-ecc\skills\motion-foundations\SKILL.md` |
| affaan-m/ECC | `motion-patterns` | Production-ready animation patterns for React / Next.js — button, modal, toast, stagger, page transitions, exit animations, scroll, and layout — built on motion-foundations tokens and springs. | `vendor\skill-sources\affaan-m-ecc\skills\motion-patterns\SKILL.md` |
| affaan-m/ECC | `motion-ui` | Production-ready UI motion system for React/Next.js. Use when implementing animations, transitions, or motion patterns. | `vendor\skill-sources\affaan-m-ecc\skills\motion-ui\SKILL.md` |
| affaan-m/ECC | `mysql-patterns` | MySQL and MariaDB schema, query, indexing, transaction, replication, and connection-pool patterns for production backends. | `vendor\skill-sources\affaan-m-ecc\skills\mysql-patterns\SKILL.md` |
| affaan-m/ECC | `nanoclaw-repl` | Operate and extend NanoClaw v2, ECC's zero-dependency session-aware REPL built on claude -p. | `vendor\skill-sources\affaan-m-ecc\skills\nanoclaw-repl\SKILL.md` |
| affaan-m/ECC | `nestjs-patterns` | NestJS architecture patterns for modules, controllers, providers, DTO validation, guards, interceptors, config, and production-grade TypeScript backends. | `vendor\skill-sources\affaan-m-ecc\skills\nestjs-patterns\SKILL.md` |
| affaan-m/ECC | `netmiko-ssh-automation` | Safe Python Netmiko patterns for read-only collection, bounded batch SSH, TextFSM parsing, guarded config changes, timeouts, and network automation error handling. | `vendor\skill-sources\affaan-m-ecc\skills\netmiko-ssh-automation\SKILL.md` |
| affaan-m/ECC | `network-bgp-diagnostics` | Diagnostics-only BGP troubleshooting patterns for neighbor state, route exchange, prefix policy, AS path inspection, and safe evidence collection. | `vendor\skill-sources\affaan-m-ecc\skills\network-bgp-diagnostics\SKILL.md` |
| affaan-m/ECC | `network-config-validation` | Pre-deployment checks for router and switch configuration, including dangerous commands, duplicate addresses, subnet overlaps, stale references, management-plane risk, and IOS-style security hygiene. | `vendor\skill-sources\affaan-m-ecc\skills\network-config-validation\SKILL.md` |
| affaan-m/ECC | `network-interface-health` | Diagnose interface errors, drops, CRCs, duplex mismatches, flapping, speed negotiation issues, and counter trends on routers, switches, and Linux hosts. | `vendor\skill-sources\affaan-m-ecc\skills\network-interface-health\SKILL.md` |
| affaan-m/ECC | `nextjs-turbopack` | Next.js 16+ and Turbopack — incremental bundling, FS caching, dev speed, and when to use Turbopack vs webpack. | `vendor\skill-sources\affaan-m-ecc\skills\nextjs-turbopack\SKILL.md` |
| affaan-m/ECC | `nodejs-keccak256` | Prevent Ethereum hashing bugs in JavaScript and TypeScript. Node's sha3-256 is NIST SHA3, not Ethereum Keccak-256, and silently breaks selectors, signatures, storage slots, and address derivation. | `vendor\skill-sources\affaan-m-ecc\skills\nodejs-keccak256\SKILL.md` |
| affaan-m/ECC | `nutrient-document-processing` | Process, convert, OCR, extract, redact, sign, and fill documents using the Nutrient DWS API. Works with PDFs, DOCX, XLSX, PPTX, HTML, and images. | `vendor\skill-sources\affaan-m-ecc\skills\nutrient-document-processing\SKILL.md` |
| affaan-m/ECC | `nuxt4-patterns` | Nuxt 4 app patterns for hydration safety, performance, route rules, lazy loading, and SSR-safe data fetching with useFetch and useAsyncData. | `vendor\skill-sources\affaan-m-ecc\skills\nuxt4-patterns\SKILL.md` |
| affaan-m/ECC | `openclaw-persona-forge` | 为 OpenClaw AI Agent 锻造完整的龙虾灵魂方案。根据用户偏好或随机抽卡， 输出身份定位、灵魂描述(SOUL.md)、角色化底线规则、名字和头像生图提示词。 如当前环境提供已审核的生图 skill，可自动生成统一风格头像图片。 当用户需要创建、设计或定制 OpenClaw 龙虾灵魂时使用。 不适用于：微调已有 SOUL.md、非 OpenClaw 平台的角色设计、纯工具型无性格 Agent。 触发词：龙虾灵魂、虾魂、OpenClaw 灵魂、养虾灵魂、龙虾角色、龙虾定位、 龙虾剧本杀角色、龙虾游戏角色、龙虾 NPC、龙虾性格、龙虾背景故事、 lobster soul、lobster character、抽卡、随机龙虾、龙虾 SOUL、gacha。 | `vendor\skill-sources\affaan-m-ecc\skills\openclaw-persona-forge\SKILL.md` |
| affaan-m/ECC | `opensource-pipeline` | Open-source pipeline: fork, sanitize, and package private projects for safe public release. Chains 3 agents (forker, sanitizer, packager). Triggers: '/opensource', 'open source this', 'make this public', 'prepare for open source'. | `vendor\skill-sources\affaan-m-ecc\skills\opensource-pipeline\SKILL.md` |
| affaan-m/ECC | `orch-add-feature` | Orchestrate building a brand-new feature end to end — research, plan, TDD implementation, review, and gated commit — by delegating each phase to the matching ECC agent. Use when adding a capability that does not exist yet. | `vendor\skill-sources\affaan-m-ecc\skills\orch-add-feature\SKILL.md` |
| affaan-m/ECC | `orch-build-mvp` | Orchestrate bootstrapping a working MVP from a design or spec document — ingest the doc, plan thin vertical slices, scaffold the first end-to-end slice, then TDD-implement, review, and gated commit. Use to turn an SDD/PRD into a running starting point. | `vendor\skill-sources\affaan-m-ecc\skills\orch-build-mvp\SKILL.md` |
| affaan-m/ECC | `orch-change-feature` | Orchestrate altering an existing, working feature to new desired behavior — update its tests to the new spec, change the implementation to match, review, and gated commit. Use when behavior is not broken but should be different. | `vendor\skill-sources\affaan-m-ecc\skills\orch-change-feature\SKILL.md` |
| affaan-m/ECC | `orch-fix-defect` | Orchestrate fixing a bug — reproduce it as a failing regression test, fix to green, review, and gated commit — by delegating each phase to the matching ECC agent. Use when existing behavior is broken or wrong. | `vendor\skill-sources\affaan-m-ecc\skills\orch-fix-defect\SKILL.md` |
| affaan-m/ECC | `orch-pipeline` | Shared orchestration engine for the orch-* skill family. Defines the gated Research-Plan-TDD-Review-Commit pipeline, the size classifier, the agent map, and the two human gates that the orch-* operation skills delegate to. Not usually invoked directly. | `vendor\skill-sources\affaan-m-ecc\skills\orch-pipeline\SKILL.md` |
| affaan-m/ECC | `orch-refine-code` | Orchestrate a behavior-preserving refactor — confirm tests are green, restructure without changing behavior, keep tests green, review, and gated commit. Use when the structure should improve but behavior must not change. | `vendor\skill-sources\affaan-m-ecc\skills\orch-refine-code\SKILL.md` |
| affaan-m/ECC | `parallel-execution-optimizer` | Use when the user wants a task done much faster through parallel work, concurrent agents, batched tool calls, isolated worktrees, or many independent verification lanes without losing correctness. | `vendor\skill-sources\affaan-m-ecc\skills\parallel-execution-optimizer\SKILL.md` |
| affaan-m/ECC | `perl-patterns` | Modern Perl 5.36+ idioms, best practices, and conventions for building robust, maintainable Perl applications. | `vendor\skill-sources\affaan-m-ecc\skills\perl-patterns\SKILL.md` |
| affaan-m/ECC | `perl-security` | Comprehensive Perl security covering taint mode, input validation, safe process execution, DBI parameterized queries, web security (XSS/SQLi/CSRF), and perlcritic security policies. | `vendor\skill-sources\affaan-m-ecc\skills\perl-security\SKILL.md` |
| affaan-m/ECC | `perl-testing` | Perl testing patterns using Test2::V0, Test::More, prove runner, mocking, coverage with Devel::Cover, and TDD methodology. | `vendor\skill-sources\affaan-m-ecc\skills\perl-testing\SKILL.md` |
| affaan-m/ECC | `plankton-code-quality` | Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude-powered fixes on every file edit via hooks. | `vendor\skill-sources\affaan-m-ecc\skills\plankton-code-quality\SKILL.md` |
| affaan-m/ECC | `plan-orchestrate` | Read a plan document, decompose it into steps, design a per-step agent chain from the ECC catalogue, and emit ready-to-paste /orchestrate custom prompts. Generative only — never invokes /orchestrate itself. Use when the user has a multi-step plan and wants to drive it through orchestrate without composing chains by hand. | `vendor\skill-sources\affaan-m-ecc\skills\plan-orchestrate\SKILL.md` |
| affaan-m/ECC | `postgres-patterns` | PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices. | `vendor\skill-sources\affaan-m-ecc\skills\postgres-patterns\SKILL.md` |
| affaan-m/ECC | `prediction-market-oracle-research` | Research prediction markets as data sources or oracle signals for products, agents, dashboards, and corporate decision intelligence. Use for source-grounded analysis of market-implied probabilities, caveats, and integration patterns without investment advice. | `vendor\skill-sources\affaan-m-ecc\skills\prediction-market-oracle-research\SKILL.md` |
| affaan-m/ECC | `prediction-market-risk-review` | Review prediction-market, basket, oracle, and trading-agent workflows for compliance, safety, data-quality, privacy, and execution risk. Use before any workflow handles venue auth, user portfolio data, API keys, or trade planning. | `vendor\skill-sources\affaan-m-ecc\skills\prediction-market-risk-review\SKILL.md` |
| affaan-m/ECC | `prisma-patterns` | Prisma ORM patterns for TypeScript backends — schema design, query optimization, transactions, pagination, and critical traps like updateMany returning count not records, $transaction timeouts, migrate dev resetting the DB, @updatedAt skipped on bulk writes, and serverless connection exhaustion. | `vendor\skill-sources\affaan-m-ecc\skills\prisma-patterns\SKILL.md` |
| affaan-m/ECC | `product-capability` | Translate PRD intent, roadmap asks, or product discussions into an implementation-ready capability plan that exposes constraints, invariants, interfaces, and unresolved decisions before multi-service work starts. Use when the user needs an ECC-native PRD-to-SRS lane instead of vague planning prose. | `vendor\skill-sources\affaan-m-ecc\skills\product-capability\SKILL.md` |
| affaan-m/ECC | `production-audit` | Local-evidence production readiness audit for shipped apps, pre-launch reviews, post-merge checks, and "what breaks in prod?" questions without sending repo data to an external audit service. | `vendor\skill-sources\affaan-m-ecc\skills\production-audit\SKILL.md` |
| affaan-m/ECC | `production-scheduling` | > | `vendor\skill-sources\affaan-m-ecc\skills\production-scheduling\SKILL.md` |
| affaan-m/ECC | `product-lens` | Use this skill to validate the "why" before building, run product diagnostics, and pressure-test product direction before the request becomes an implementation contract. | `vendor\skill-sources\affaan-m-ecc\skills\product-lens\SKILL.md` |
| affaan-m/ECC | `project-flow-ops` | Operate execution flow across GitHub and Linear by triaging issues and pull requests, linking active work, and keeping GitHub public-facing while Linear remains the internal execution layer. Use when the user wants backlog control, PR triage, or GitHub-to-Linear coordination. | `vendor\skill-sources\affaan-m-ecc\skills\project-flow-ops\SKILL.md` |
| affaan-m/ECC | `prompt-optimizer` | >- | `vendor\skill-sources\affaan-m-ecc\skills\prompt-optimizer\SKILL.md` |
| affaan-m/ECC | `python-patterns` | Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications. | `vendor\skill-sources\affaan-m-ecc\skills\python-patterns\SKILL.md` |
| affaan-m/ECC | `python-testing` | Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements. | `vendor\skill-sources\affaan-m-ecc\skills\python-testing\SKILL.md` |
| affaan-m/ECC | `pytorch-patterns` | PyTorch deep learning patterns and best practices for building robust, efficient, and reproducible training pipelines, model architectures, and data loading. | `vendor\skill-sources\affaan-m-ecc\skills\pytorch-patterns\SKILL.md` |
| affaan-m/ECC | `quality-nonconformance` | > | `vendor\skill-sources\affaan-m-ecc\skills\quality-nonconformance\SKILL.md` |
| affaan-m/ECC | `quarkus-patterns` | Quarkus 3.x LTS architecture patterns with Camel for messaging, RESTful API design, CDI services, data access with Panache, and async processing. Use for Java Quarkus backend work with event-driven architectures. | `vendor\skill-sources\affaan-m-ecc\skills\quarkus-patterns\SKILL.md` |
| affaan-m/ECC | `quarkus-security` | Quarkus Security best practices for authentication, authorization, JWT/OIDC, RBAC, input validation, CSRF, secrets management, and dependency security. | `vendor\skill-sources\affaan-m-ecc\skills\quarkus-security\SKILL.md` |
| affaan-m/ECC | `quarkus-tdd` | Test-driven development for Quarkus 3.x LTS using JUnit 5, Mockito, REST Assured, Camel testing, and JaCoCo. Use when adding features, fixing bugs, or refactoring event-driven services. | `vendor\skill-sources\affaan-m-ecc\skills\quarkus-tdd\SKILL.md` |
| affaan-m/ECC | `quarkus-verification` | Verification loop for Quarkus projects: build, static analysis, tests with coverage, security scans, native compilation, and diff review before release or PR. | `vendor\skill-sources\affaan-m-ecc\skills\quarkus-verification\SKILL.md` |
| affaan-m/ECC | `ralphinho-rfc-pipeline` | RFC-driven multi-agent DAG execution pattern with quality gates, merge queues, and work unit orchestration. | `vendor\skill-sources\affaan-m-ecc\skills\ralphinho-rfc-pipeline\SKILL.md` |
| affaan-m/ECC | `react-patterns` | React 18/19 patterns including hooks discipline, server/client component boundaries, Suspense + error boundaries, form actions, data fetching, state management decision trees, and accessibility-first composition. Use when writing or reviewing React components. | `vendor\skill-sources\affaan-m-ecc\skills\react-patterns\SKILL.md` |
| affaan-m/ECC | `react-performance` | React and Next.js performance optimization patterns adapted from Vercel Engineering's React Best Practices (https://github.com/vercel-labs/agent-skills). Organizes 70+ rules across 8 priority categories — waterfalls, bundle size, server-side, client fetching, re-render, rendering, JS micro-perf, advanced. Use when writing, reviewing, or refactoring React/Next.js code for performance. | `vendor\skill-sources\affaan-m-ecc\skills\react-performance\SKILL.md` |
| affaan-m/ECC | `react-testing` | React component testing with React Testing Library, Vitest/Jest, MSW for network mocking, accessibility assertions with axe, and the decision boundary between component tests and Playwright/Cypress end-to-end runs. Use when writing or fixing tests for React components, hooks, or pages. | `vendor\skill-sources\affaan-m-ecc\skills\react-testing\SKILL.md` |
| affaan-m/ECC | `recsys-pipeline-architect` | Design composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect framework popularized by xAI's open-sourced For You algorithm. Use this skill whenever the user is building any system that picks "the top K items for a (user, context)" — social feeds, content CMSs, RAG rerankers, task prioritizers, notification triage, search reranking, ad ranking. | `vendor\skill-sources\affaan-m-ecc\skills\recsys-pipeline-architect\SKILL.md` |
| affaan-m/ECC | `recursive-decision-ledger` | Use when the user asks for repeated rollouts, marked decision processes, high-dimensional search, stochastic optimization, local-optima exploration, ensemble comparison, or recursive reasoning with a visible evidence trail. | `vendor\skill-sources\affaan-m-ecc\skills\recursive-decision-ledger\SKILL.md` |
| affaan-m/ECC | `redis-patterns` | Redis data structure patterns, caching strategies, distributed locks, rate limiting, pub/sub, and connection management for production applications. | `vendor\skill-sources\affaan-m-ecc\skills\redis-patterns\SKILL.md` |
| affaan-m/ECC | `regex-vs-llm-structured-text` | Decision framework for choosing between regex and LLM when parsing structured text — start with regex, add LLM only for low-confidence edge cases. | `vendor\skill-sources\affaan-m-ecc\skills\regex-vs-llm-structured-text\SKILL.md` |
| affaan-m/ECC | `remotion-video-creation` | Best practices for Remotion - Video creation in React. 29 domain-specific rules covering 3D, animations, audio, captions, charts, transitions, and more. | `vendor\skill-sources\affaan-m-ecc\skills\remotion-video-creation\SKILL.md` |
| affaan-m/ECC | `repo-scan` | Cross-stack source code asset audit — classifies every file, detects embedded third-party libraries, and delivers actionable four-level verdicts per module with interactive HTML reports. | `vendor\skill-sources\affaan-m-ecc\skills\repo-scan\SKILL.md` |
| affaan-m/ECC | `research-ops` | Evidence-first current-state research workflow for ECC. Use when the user wants fresh facts, comparisons, enrichment, or a recommendation built from current public evidence and any supplied local context. | `vendor\skill-sources\affaan-m-ecc\skills\research-ops\SKILL.md` |
| affaan-m/ECC | `returns-reverse-logistics` | > | `vendor\skill-sources\affaan-m-ecc\skills\returns-reverse-logistics\SKILL.md` |
| affaan-m/ECC | `rules-distill` | Scan skills to extract cross-cutting principles and distill them into rules — append, revise, or create new rule files | `vendor\skill-sources\affaan-m-ecc\skills\rules-distill\SKILL.md` |
| affaan-m/ECC | `rust-patterns` | Idiomatic Rust patterns, ownership, error handling, traits, concurrency, and best practices for building safe, performant applications. | `vendor\skill-sources\affaan-m-ecc\skills\rust-patterns\SKILL.md` |
| affaan-m/ECC | `rust-testing` | Rust testing patterns including unit tests, integration tests, async testing, property-based testing, mocking, and coverage. Follows TDD methodology. | `vendor\skill-sources\affaan-m-ecc\skills\rust-testing\SKILL.md` |
| affaan-m/ECC | `safety-guard` | Use this skill to prevent destructive operations when working on production systems or running agents autonomously. | `vendor\skill-sources\affaan-m-ecc\skills\safety-guard\SKILL.md` |
| affaan-m/ECC | `santa-method` | Multi-agent adversarial verification with convergence loop. Two independent review agents must both pass before output ships. | `vendor\skill-sources\affaan-m-ecc\skills\santa-method\SKILL.md` |
| affaan-m/ECC | `scientific-db-pubmed-database` | Direct PubMed and NCBI E-utilities search workflows for biomedical literature, MeSH queries, PMID lookup, citation retrieval, and API-backed literature monitoring. | `vendor\skill-sources\affaan-m-ecc\skills\scientific-db-pubmed-database\SKILL.md` |
| affaan-m/ECC | `scientific-db-uspto-database` | USPTO patent and trademark data workflow for official record lookup, PatentSearch queries, TSDR checks, assignment data, and reproducible IP research logs. | `vendor\skill-sources\affaan-m-ecc\skills\scientific-db-uspto-database\SKILL.md` |
| affaan-m/ECC | `scientific-pkg-gget` | gget CLI and Python workflow for quick genomic database queries, sequence lookup, BLAST-style searches, enrichment checks, and reproducible bioinformatics evidence logs. | `vendor\skill-sources\affaan-m-ecc\skills\scientific-pkg-gget\SKILL.md` |
| affaan-m/ECC | `scientific-thinking-literature-review` | Systematic literature-review workflow for academic, biomedical, technical, and scientific topics, including search planning, source screening, synthesis, citation checks, and evidence logging. | `vendor\skill-sources\affaan-m-ecc\skills\scientific-thinking-literature-review\SKILL.md` |
| affaan-m/ECC | `scientific-thinking-scholar-evaluation` | Structured scholarly-work evaluation for papers, proposals, literature reviews, methods sections, evidence quality, citation support, and research-writing feedback. | `vendor\skill-sources\affaan-m-ecc\skills\scientific-thinking-scholar-evaluation\SKILL.md` |
| affaan-m/ECC | `search-first` | Research-before-coding workflow. Search for existing tools, libraries, and patterns before writing custom code. Invokes the researcher agent. | `vendor\skill-sources\affaan-m-ecc\skills\search-first\SKILL.md` |
| affaan-m/ECC | `security-bounty-hunter` | Hunt for exploitable, bounty-worthy security issues in repositories. Focuses on remotely reachable vulnerabilities that qualify for real reports instead of noisy local-only findings. | `vendor\skill-sources\affaan-m-ecc\skills\security-bounty-hunter\SKILL.md` |
| affaan-m/ECC | `security-review` | Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns. | `vendor\skill-sources\affaan-m-ecc\skills\security-review\SKILL.md` |
| affaan-m/ECC | `security-scan` | Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, misconfigurations, and injection risks using AgentShield. Checks CLAUDE.md, settings.json, MCP servers, hooks, and agent definitions. | `vendor\skill-sources\affaan-m-ecc\skills\security-scan\SKILL.md` |
| affaan-m/ECC | `seo` | Audit, plan, and implement SEO improvements across technical SEO, on-page optimization, structured data, Core Web Vitals, and content strategy. Use when the user wants better search visibility, SEO remediation, schema markup, sitemap/robots work, or keyword mapping. | `vendor\skill-sources\affaan-m-ecc\skills\seo\SKILL.md` |
| affaan-m/ECC | `skill-comply` | Visualize whether skills, rules, and agent definitions are actually followed — auto-generates scenarios at 3 prompt strictness levels, runs agents, classifies behavioral sequences, and reports compliance rates with full tool call timelines | `vendor\skill-sources\affaan-m-ecc\skills\skill-comply\SKILL.md` |
| affaan-m/ECC | `skill-scout` | Search existing local, marketplace, GitHub, and web skill sources before creating a new skill. Use when the user wants to create, build, fork, or find a skill for a workflow. | `vendor\skill-sources\affaan-m-ecc\skills\skill-scout\SKILL.md` |
| affaan-m/ECC | `skill-stocktake` | Use when auditing Claude skills and commands for quality. Supports Quick Scan (changed skills only) and Full Stocktake modes with sequential subagent batch evaluation. | `vendor\skill-sources\affaan-m-ecc\skills\skill-stocktake\SKILL.md` |
| affaan-m/ECC | `social-graph-ranker` | Weighted social-graph ranking for warm intro discovery, bridge scoring, and network gap analysis across X and LinkedIn. Use when the user wants the reusable graph-ranking engine itself, not the broader outreach or network-maintenance workflow layered on top of it. | `vendor\skill-sources\affaan-m-ecc\skills\social-graph-ranker\SKILL.md` |
| affaan-m/ECC | `social-publisher` | Agent-driven scheduling and publishing of social media posts across 13 platforms via SocialClaw. Use when the user wants to publish to X, LinkedIn, Instagram, Facebook Pages, TikTok, Discord, Telegram, YouTube, Reddit, WordPress, or Pinterest — or when managing campaigns, uploading media, or monitoring post delivery status. | `vendor\skill-sources\affaan-m-ecc\skills\social-publisher\SKILL.md` |
| affaan-m/ECC | `springboot-patterns` | Spring Boot architecture patterns, REST API design, layered services, data access, caching, async processing, and logging. Use for Java Spring Boot backend work. | `vendor\skill-sources\affaan-m-ecc\skills\springboot-patterns\SKILL.md` |
| affaan-m/ECC | `springboot-security` | Spring Security best practices for authn/authz, validation, CSRF, secrets, headers, rate limiting, and dependency security in Java Spring Boot services. | `vendor\skill-sources\affaan-m-ecc\skills\springboot-security\SKILL.md` |
| affaan-m/ECC | `springboot-tdd` | Test-driven development for Spring Boot using JUnit 5, Mockito, MockMvc, Testcontainers, and JaCoCo. Use when adding features, fixing bugs, or refactoring. | `vendor\skill-sources\affaan-m-ecc\skills\springboot-tdd\SKILL.md` |
| affaan-m/ECC | `springboot-verification` | Verification loop for Spring Boot projects: build, static analysis, tests with coverage, security scans, and diff review before release or PR. | `vendor\skill-sources\affaan-m-ecc\skills\springboot-verification\SKILL.md` |
| affaan-m/ECC | `strategic-compact` | Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction. | `vendor\skill-sources\affaan-m-ecc\skills\strategic-compact\SKILL.md` |
| affaan-m/ECC | `swift-actor-persistence` | Thread-safe data persistence in Swift using actors — in-memory cache with file-backed storage, eliminating data races by design. | `vendor\skill-sources\affaan-m-ecc\skills\swift-actor-persistence\SKILL.md` |
| affaan-m/ECC | `swift-concurrency-6-2` | Swift 6.2 Approachable Concurrency — single-threaded by default, @concurrent for explicit background offloading, isolated conformances for main actor types. | `vendor\skill-sources\affaan-m-ecc\skills\swift-concurrency-6-2\SKILL.md` |
| affaan-m/ECC | `swift-protocol-di-testing` | Protocol-based dependency injection for testable Swift code — mock file system, network, and external APIs using focused protocols and Swift Testing. | `vendor\skill-sources\affaan-m-ecc\skills\swift-protocol-di-testing\SKILL.md` |
| affaan-m/ECC | `swiftui-patterns` | SwiftUI architecture patterns, state management with @Observable, view composition, navigation, performance optimization, and modern iOS/macOS UI best practices. | `vendor\skill-sources\affaan-m-ecc\skills\swiftui-patterns\SKILL.md` |
| affaan-m/ECC | `taste` | A creative-direction (taste) layer for music videos and short-form edits in the angelcore / cloud-trance / hyperpop visual family. Distills a named-genre aesthetic vocabulary, a mood + color + light system, and a beat-synced editing grammar, then chains ECC's video skills (video-editing, fal-ai-media, remotion-video-creation, motion-*, content-engine) into one production pipeline. Use when the work is not just making a video function but making it feel intentional, when building a music video, a fancam/edit, a moodboard-driven reel, or when choosing a coherent visual direction for AI-generated b-roll. | `vendor\skill-sources\affaan-m-ecc\skills\taste\SKILL.md` |
| affaan-m/ECC | `tdd-workflow` | Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests. | `vendor\skill-sources\affaan-m-ecc\skills\tdd-workflow\SKILL.md` |
| affaan-m/ECC | `team-agent-orchestration` | Run team-based orchestration for agent squads using work items, ownership, agent Kanban, merge gates, and control pane handoffs. | `vendor\skill-sources\affaan-m-ecc\skills\team-agent-orchestration\SKILL.md` |
| affaan-m/ECC | `team-builder` | Interactive agent picker for composing and dispatching parallel teams | `vendor\skill-sources\affaan-m-ecc\skills\team-builder\SKILL.md` |
| affaan-m/ECC | `terminal-ops` | Evidence-first repo execution workflow for ECC. Use when the user wants a command run, a repo checked, a CI failure debugged, or a narrow fix pushed with exact proof of what was executed and verified. | `vendor\skill-sources\affaan-m-ecc\skills\terminal-ops\SKILL.md` |
| affaan-m/ECC | `tinystruct-patterns` | Expert guidance for developing with the tinystruct Java framework. Use when working on the tinystruct codebase or any project built on tinystruct — including creating Application classes, @Action-mapped routes, unit tests, ActionRegistry, HTTP/CLI dual-mode handling, the built-in HTTP server, the event system, JSON with Builder/Builders, database persistence with AbstractData, POJO generation, Server-Sent Events (SSE), file uploads, and outbound HTTP networking. | `vendor\skill-sources\affaan-m-ecc\skills\tinystruct-patterns\SKILL.md` |
| affaan-m/ECC | `token-budget-advisor` | >- | `vendor\skill-sources\affaan-m-ecc\skills\token-budget-advisor\SKILL.md` |
| affaan-m/ECC | `ui-demo` | Record polished UI demo videos using Playwright. Use when the user asks to create a demo, walkthrough, screen recording, or tutorial video of a web application. Produces WebM videos with visible cursor, natural pacing, and professional feel. | `vendor\skill-sources\affaan-m-ecc\skills\ui-demo\SKILL.md` |
| affaan-m/ECC | `ui-to-vue` | Use when the user has UI screenshots or design exports that need batch conversion into Vue 3 components, especially with Vant, Element Plus, or Ant Design Vue. | `vendor\skill-sources\affaan-m-ecc\skills\ui-to-vue\SKILL.md` |
| affaan-m/ECC | `uncloud` | Use when managing an Uncloud cluster — deploying services, configuring Caddy ingress, adding static proxy routes for non-cluster devices, publishing ports, scaling, inspecting logs, or managing machines and volumes with the `uc` CLI. | `vendor\skill-sources\affaan-m-ecc\skills\uncloud\SKILL.md` |
| affaan-m/ECC | `unified-notifications-ops` | Operate notifications as one ECC-native workflow across GitHub, Linear, desktop alerts, hooks, and connected communication surfaces. Use when the real problem is alert routing, deduplication, escalation, or inbox collapse. | `vendor\skill-sources\affaan-m-ecc\skills\unified-notifications-ops\SKILL.md` |
| affaan-m/ECC | `verification-loop` | A comprehensive verification system for Claude Code sessions. | `vendor\skill-sources\affaan-m-ecc\skills\verification-loop\SKILL.md` |
| affaan-m/ECC | `videodb` | See, Understand, Act on video and audio. See- ingest from local files, URLs, RTSP/live feeds, or live record desktop; return realtime context and playable stream links. Understand- extract frames, build visual/semantic/temporal indexes, and search moments with timestamps and auto-clips. Act- transcode and normalize (codec, fps, resolution, aspect ratio), perform timeline edits (subtitles, text/image overlays, branding, audio overlays, dubbing, translation), generate media assets (image, audio, video), and create real time alerts for events from live streams or desktop capture. | `vendor\skill-sources\affaan-m-ecc\skills\videodb\SKILL.md` |
| affaan-m/ECC | `video-editing` | AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. Covers the full pipeline from raw capture through FFmpeg, Remotion, ElevenLabs, fal.ai, and final polish in Descript or CapCut. Use when the user wants to edit video, cut footage, create vlogs, or build video content. | `vendor\skill-sources\affaan-m-ecc\skills\video-editing\SKILL.md` |
| affaan-m/ECC | `visa-doc-translate` | Translate visa application documents (images) to English and create a bilingual PDF with original and translation | `vendor\skill-sources\affaan-m-ecc\skills\visa-doc-translate\SKILL.md` |
| affaan-m/ECC | `vite-patterns` | Vite build tool patterns including config, plugins, HMR, env variables, proxy setup, SSR, library mode, dependency pre-bundling, and build optimization. Activate when working with vite.config.ts, Vite plugins, or Vite-based projects. | `vendor\skill-sources\affaan-m-ecc\skills\vite-patterns\SKILL.md` |
| affaan-m/ECC | `vue-patterns` | Vue.js 3 Composition API patterns, component architecture, reactivity best practices, Pinia state management, Vue Router navigation, and Nuxt SSR patterns. Activates for Vue, Nuxt, Vite, or Pinia projects. | `vendor\skill-sources\affaan-m-ecc\skills\vue-patterns\SKILL.md` |
| affaan-m/ECC | `windows-desktop-e2e` | E2E testing for Windows native desktop apps (WPF, WinForms, Win32/MFC, Qt) using pywinauto and Windows UI Automation. | `vendor\skill-sources\affaan-m-ecc\skills\windows-desktop-e2e\SKILL.md` |
| affaan-m/ECC | `workspace-surface-audit` | Audit the active repo, MCP servers, plugins, connectors, env surfaces, and harness setup, then recommend the highest-value ECC-native skills, hooks, agents, and operator workflows. Use when the user wants help setting up Claude Code or understanding what capabilities are actually available in their environment. | `vendor\skill-sources\affaan-m-ecc\skills\workspace-surface-audit\SKILL.md` |
| affaan-m/ECC | `x-api` | X/Twitter API integration for posting tweets, threads, reading timelines, search, and analytics. Covers OAuth auth patterns, rate limits, and platform-native content posting. Use when the user wants to interact with X programmatically. | `vendor\skill-sources\affaan-m-ecc\skills\x-api\SKILL.md` |
| DietrichGebert/ponytail | `ponytail` | Forces the laziest solution that actually works, simplest, shortest, most minimal. Channels a senior dev who has seen everything: question whether the task needs to exist at all (YAGNI), reach for the standard library before custom code, native platform features before dependencies, one line before fifty. Supports intensity levels: lite, full (default), ultra. Use whenever the user says "ponytail", "be lazy", "lazy mode", "simplest solution", "minimal solution", "yagni", "do less", or "shortest path", and whenever they complain about over-engineering, bloat, boilerplate, or unnecessary dependencies. | `vendor\skill-sources\ponytail\skills\ponytail\SKILL.md` |
| DietrichGebert/ponytail | `ponytail-audit` | Whole-repo audit for over-engineering. Like ponytail-review, but scans the entire codebase instead of a diff: a ranked list of what to delete, simplify, or replace with stdlib/native equivalents. Use when the user says "audit this codebase", "audit for over-engineering", "what can I delete from this repo", "find bloat", "ponytail-audit", or "/ponytail-audit". One-shot report, does not apply fixes. | `vendor\skill-sources\ponytail\skills\ponytail-audit\SKILL.md` |
| DietrichGebert/ponytail | `ponytail-debt` | Harvest every `ponytail:` comment in the codebase into a debt ledger, so the deliberate shortcuts and deferrals ponytail leaves behind get tracked instead of rotting into "later means never". Use when the user says "ponytail debt", "/ponytail-debt", "what did ponytail defer", "list the shortcuts", "ponytail ledger", or "what did we mark to do later". One-shot report, changes nothing. | `vendor\skill-sources\ponytail\skills\ponytail-debt\SKILL.md` |
| DietrichGebert/ponytail | `ponytail-help` | Quick-reference card for all ponytail modes, skills, and commands. One-shot display, not a persistent mode. Trigger: /ponytail-help, "ponytail help", "what ponytail commands", "how do I use ponytail". | `vendor\skill-sources\ponytail\skills\ponytail-help\SKILL.md` |
| DietrichGebert/ponytail | `ponytail-review` | Code review focused exclusively on over-engineering. Finds what to delete: reinvented standard library, unneeded dependencies, speculative abstractions, dead flexibility. One line per finding: location, what to cut, what replaces it. Use when the user says "review for over-engineering", "what can we delete", "is this over-engineered", "simplify review", or invokes /ponytail-review. Complements correctness-focused review, this one only hunts complexity. | `vendor\skill-sources\ponytail\skills\ponytail-review\SKILL.md` |

