@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PS_SCRIPT=%SCRIPT_DIR%Deploy-SkillSet.ps1"

if not exist "%PS_SCRIPT%" (
    echo Missing PowerShell implementation: "%PS_SCRIPT%" 1>&2
    exit /b 1
)

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%" %*
exit /b %ERRORLEVEL%
