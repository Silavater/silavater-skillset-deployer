@echo off
setlocal

where py >nul 2>nul
if not errorlevel 1 (
    py -3 --version >nul 2>nul
    if not errorlevel 1 (
        py -3 "%~dp0SkillDeployer-TUI.py" %*
        exit /b
    )
)

where python >nul 2>nul
if not errorlevel 1 (
    python --version >nul 2>nul
    if not errorlevel 1 (
        python "%~dp0SkillDeployer-TUI.py" %*
        exit /b
    )
)

echo Python 3 was not found. Install Python 3, then rerun this command.
exit /b 1
