# Silavater 技能集部署器

適用於 OpenCode / Claude Code 類代理環境的可攜式本機技能集部署套件。

這個資料夾設計成可以複製到其他專案中，然後從該專案內使用本機鏡像儲存庫部署已整理好的技能集。

## 內容

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
      └─ affaan-m-ecc/
```

## 各部分用途

- `vendor/skill-sources/`：上游技能儲存庫的本機鏡像。這是可離線、可快取的真實來源。
- `scripts/Deploy-SkillSet.py`：建議使用的部署器，支援互動選單、整理好的 skill set、單一 skill、指定 target root 與 dry run。
- `scripts/Deploy-SkillSet-Py.cmd`：Windows 上呼叫 Python 部署器的啟動器。
- `scripts/SkillDeployer-TUI.py`：雙模式終端 UI，包含 `SkillSetDeployMode` 與 `SingleSkillDeployMode`。
- `scripts/SkillDeployer-TUI.cmd`：Windows 上呼叫終端 UI 的啟動器。
- `scripts/Deploy-SkillSet.cmd`：舊版 PowerShell 部署器的 Windows 啟動器。
- `scripts/Deploy-SkillSet.ps1`：舊版 PowerShell 實作，透過 `npx skills add` 從本機鏡像部署已整理好的技能集。
- `scripts/Update-SkillSources.py`：用 Python 更新兩個本機上游 mirror 的腳本。
- `scripts/Update-SkillSources.cmd`：Windows 上呼叫 Python 更新腳本的啟動器。
- `docs/SKILL_CATALOG.md`：自動產生的英文技能目錄，包含可用技能、建議技能集、部署指令、已知注意事項與上游來源／授權說明。
- `docs/SKILL_CATALOG.zh-TW.md`：繁體中文技能目錄。
- `THIRD_PARTY_NOTICES.md`：第三方來源、授權與本機鏡像聲明。
- `README.md`：英文可攜式使用指南。
- `README.zh-TW.md`：本繁體中文使用指南。

## 環境需求

一般部署需要：

- 主要支援 Windows，因為本套件提供的是 `.cmd` 啟動器。
- Python 3，需可透過 `py -3` 或 `python` 執行。
- Node.js / npm，且需包含 `npx`。
- 第一次讓 `npx skills` 解析 `skills` 套件時需要網路。

更新本機 mirror 需要：

- Git，需可透過 `git` 執行。
- fetch 或 clone 上游 repository 時需要能連到 GitHub。

選用 / 舊版：

- PowerShell 5+ 或 PowerShell 7+ 只在使用舊版 `Deploy-SkillSet.ps1` 部署器，以及重新產生 catalog 時需要。

快速檢查環境：

```cmd
py -3 --version
python --version
node --version
npm --version
npx --version
git --version
```

`py -3` 和 `python` 只要其中一個能正常執行即可。Windows 啟動器會先嘗試 `py -3`，再嘗試 `python`。

## Attribution / 來源與致謝

This project packages local mirrors and deployment helpers for selected agent skills from:

| Upstream | Description | License | Local path |
|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | Skills for real engineering workflows | MIT | `vendor/skill-sources/mattpocock-skills` |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | Cross-harness agent workflow system and skill catalog | MIT | `vendor/skill-sources/affaan-m-ecc` |

`vendor/skill-sources/` 內的 skill 來源於上述上游專案。本專案僅提供本機 mirror、skill set 分組、可攜式部署 wrapper 與文件，並非上述 repository 的官方發行版。

原始內容、授權與歷史紀錄請以上游 repositories 為準。若使用、修改或重新散布本專案，請保留上游 LICENSE 與 attribution notices。詳情請見 `THIRD_PARTY_NOTICES.md` 與各 upstream `LICENSE` 檔案。

## Disclaimer / 非官方聲明

This is an unofficial deployment package. It is not an official distribution of `mattpocock/skills` or `affaan-m/ECC`, and it is not affiliated with, endorsed by, or maintained by the upstream authors unless explicitly stated.

本專案不是 `mattpocock/skills` 或 `affaan-m/ECC` 的官方發行版。原始 skills 的 bug report 或 feature request 請回報至上游 repositories；此打包／部署腳本相關問題則請回報到本 repository。

## 從目標專案快速部署

建議方式：把這個套件放在目標專案內，但從目標專案 root 執行部署器。這樣 project scope 會安裝到目標專案，而不是安裝到 deployer 資料夾本身。

部署前，請先確認上方環境需求已可用。

fresh clone 不會包含 `vendor/skill-sources/`。TUI 啟動時會先檢查本機 mirror；如果 `vendor/` 不存在、是空的，或找不到可用的 skill mirror，它會詢問是否先執行 updater 再繼續。

從目標專案 root 開始：

```cmd
cd "D:\projects\target-project"

# TUI：SkillSetDeployMode / SingleSkillDeployMode
.\silavater-skillset-deployer\scripts\SkillDeployer-TUI.cmd
```

若要直接使用 CLI，fresh clone 時請先 bootstrap 本機 mirror：

```cmd
cd "D:\projects\target-project\silavater-skillset-deployer"
.\scripts\Update-SkillSources.cmd
cd "D:\projects\target-project"

# 只預覽，不做任何變更
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --set env-setup --dry-run

# 將 env-setup 安裝到目標專案
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --set env-setup
```

Python 部署器會使用自己套件內的 `vendor/skill-sources/` 作為 source root。target root 預設是目前所在目錄。如果你是在 `silavater-skillset-deployer` 裡面執行，請用 `--target` 避免安裝到 deployer 資料夾：

```cmd
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --target "D:\projects\target-project"
```

對於 project-scope 安裝，Python 部署器會拒絕安裝到 deployer 資料夾本身；除非你明確加上 `--allow-deployer-target`。

腳本預設使用 `--agent opencode`。若要部署到所有支援的代理操作介面：

```cmd
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --set env-setup --agent *
```

列出可選項目：

```cmd
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --list sets
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --list skills
```

不進互動選單，直接部署單一或多個 skill：

```cmd
.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --skill matt:handoff --skill ecc:terminal-ops
```

部署模式速查：

| 模式 | 指令 |
|---|---|
| TUI 選單 | `.\silavater-skillset-deployer\scripts\SkillDeployer-TUI.cmd` |
| 整理好的 skill set | `.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --set env-setup` |
| 單一或多個 skill | `.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --skill matt:handoff --skill ecc:terminal-ops` |
| 明確指定目標 | `.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --target "D:\projects\target-project"` |
| 只預覽 | `.\silavater-skillset-deployer\scripts\Deploy-SkillSet-Py.cmd --set env-setup --dry-run` |

## 更新本機上游 mirror

當上游技能 repository 有更新時，可以一鍵更新兩個本機 mirror：

```cmd
.\scripts\Update-SkillSources.cmd
```

需求：Git 與 Python 3。Windows 上 `.cmd` 啟動器會先嘗試 `py -3`，再嘗試 `python`。

也可以直接呼叫 Python：

```cmd
py -3 .\scripts\Update-SkillSources.py
```

只預覽要執行的更新指令，不連網、不改檔案：

```cmd
.\scripts\Update-SkillSources.cmd --dry-run
```

只更新其中一個 mirror：

```cmd
.\scripts\Update-SkillSources.cmd --repo mattpocock-skills
.\scripts\Update-SkillSources.cmd --repo affaan-m-ecc
```

更新腳本管理的來源是：

- `vendor/skill-sources/mattpocock-skills`：`https://github.com/mattpocock/skills.git`
- `vendor/skill-sources/affaan-m-ecc`：`https://github.com/affaan-m/ECC.git`

如果 mirror 有本機變更、origin URL 不符合、目前不在預期的 `main` 分支，或分支歷史已經 diverged，腳本會拒絕更新，避免覆蓋手動修改。Git 指令會使用單次程序的 `safe.directory` 設定，因此能處理 Windows 複製過來後 owner 不一致的 checkout，而不需要修改全域 Git 設定。

如果 deploy 失敗並提示缺少 local skill sources，請先執行這個 updater。`vendor/` 目錄刻意不追蹤在此 repository 裡。

TUI 會自動做同樣的 mirror 檢查。啟動時如果偵測到缺少或不完整的本機 mirror，會詢問是否更新；如果後續 deploy command 失敗，也會詢問是否執行 updater 並重試一次。

## 搬移到其他專案

將整個資料夾複製到目標專案：

```powershell
Copy-Item -Recurse -Force ".\silavater-skillset-deployer" "D:\projects\target-project\silavater-skillset-deployer"
```

接著從複製後的資料夾內執行：

```cmd
cd "D:\projects\target-project\silavater-skillset-deployer"
.\scripts\Update-SkillSources.cmd
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --target "D:\projects\target-project" --dry-run
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --target "D:\projects\target-project"
```

重要：project scope 會安裝到 target root。Python 部署器預設 target 是目前所在目錄，也可以用 `--target` 明確指定。

也可以省略手動 update，直接從目標專案 root 啟動 TUI；需要 mirror 時它會詢問是否 bootstrap：

```cmd
cd "D:\projects\target-project"
.\silavater-skillset-deployer\scripts\SkillDeployer-TUI.cmd
```

## 目標專案的建議安裝方式

對於目標專案根目錄，建議使用下列結構：

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

然後執行：

```cmd
cd "D:\projects\target-project"
.\silavater-skillset-deployer\scripts\SkillDeployer-TUI.cmd
```

## 可用的整理技能集

| 技能集 | 用途 |
|---|---|
| `core-dev` | 日常開發：程式碼理解、除錯、TDD、交接與驗證。 |
| `env-setup` | 環境設定：CLI／套件／工作區稽核、文件查詢與安全防護。 |
| `research` | 先搜尋再研究、來源蒐集、文件查詢與決策摘要。 |
| `security` | 秘密資訊、MCP、設定、hooks、輸入邊界與危險操作審查。 |
| `frontend` | React／Next、無障礙、效能、動效與 UI 細節打磨。 |
| `backend-ts` | TypeScript 後端：API、資料庫、ORM、快取、Node／Next／Nest。 |
| `python` | Python 慣用寫法、pytest、Django、資料／機器學習工作流程。 |
| `agent-ops` | 技能偵察、盤點、上下文、平行化與本機知識管理。 |
| `matt-all` | 本機鏡像中的所有主要 Matt Pocock 技能。 |
| `ecc-all` | 本機鏡像中的所有主要 ECC 技能。 |
| `all` | 兩個鏡像中的所有主要技能。 |

除非你刻意需要非常大的啟用技能範圍，否則請避免使用 `ecc-all` 或 `all`。

## 重新整理技能目錄

目錄產生目前仍由舊版 PowerShell 實作處理：

```cmd
.\scripts\Deploy-SkillSet.cmd -UpdateCatalog -DryRun
```

## 驗證套件健康狀態

```powershell
powershell -NoProfile -Command "[scriptblock]::Create((Get-Content -LiteralPath '.\scripts\Deploy-SkillSet.ps1' -Raw)) | Out-Null; 'parse-ok'"
.\scripts\Update-SkillSources.cmd --dry-run
.\scripts\Deploy-SkillSet-Py.cmd --set env-setup --dry-run
```

若需要使用舊版 PowerShell 部署器，請使用 `.cmd` 啟動器或單次程序的 bypass，而不是修改整台機器的系統原則：

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\Deploy-SkillSet.ps1 -Set env-setup -Scope project -DryRun
```

## 已知注意事項：`reasoning part 0 not found`

這通常是 session viewer／gateway／模型 fallback 的中繼資料解析問題。它表示呼叫端嘗試讀取 `reasoning[0]`，但模型回應中沒有 reasoning 區段。如果 CLI 指令已完成且檔案有產出，通常不會阻擋此部署器運作。

## CC Switch

CC Switch 是另一個環境／模型／設定切換工具。它值得之後評估，但不是這個本機技能部署器的替代品。



