@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NUNES AUTONOMOUS FLEET - LIVE SYSTEM DETAILS & STATUS (v8.5.0 Quantum)
color 0B
cls

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0show_status.ps1"

if %errorlevel% neq 0 (
    echo.
    echo [!] Running fallback status query...
    echo Computer Name : %COMPUTERNAME%
    echo Current User  : %USERNAME%
    echo System Drive  : %SystemDrive%
    echo.
    pause
)
exit /b 0
