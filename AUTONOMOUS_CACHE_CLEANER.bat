@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NUNES AUTONOMOUS FLEET - INSTANT CONNECT & CLEAN
color 0B
cls

echo ===============================================================================
echo       NUNES AUTONOMOUS FLEET - SAFE CLEAN & LIVE TELEMETRY (v10.1)
echo ===============================================================================
echo.
echo [*] Initializing safe clean & dashboard synchronization...
echo [*] Computer Name: %COMPUTERNAME%
echo.

if exist "%~dp0CONNECT_THIS_PC.bat" (
    call "%~dp0CONNECT_THIS_PC.bat" %*
    exit /b %errorlevel%
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0nunes_fleet_agent.ps1"
exit /b %errorlevel%
