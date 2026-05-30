@echo off
chcp 65001 >nul
title ALVR Fix — port 8082

:: Self-elevate to Administrator (required to kill SteamVR processes)
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator rights...
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"

echo.
echo  ALVR auto-fix starting...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0alvr-fix-port-8082.ps1"

exit /b
