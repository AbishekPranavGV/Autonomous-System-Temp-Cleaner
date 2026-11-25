@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NUNES AUTONOMOUS FLEET - 1-CLICK INSTANT CONNECT & CLEAN
color 0B
cls

echo ===============================================================================
echo       NUNES AUTONOMOUS FLEET - 1-CLICK INSTANT CONNECT & AUTO-CLEAN (v10.1)
echo ===============================================================================
echo.
echo [*] Initializing fleet connection for this machine...
echo [*] Computer Name: %COMPUTERNAME%
echo [*] User Account : %USERNAME%
echo.

if exist "%~dp0CONNECT_THIS_PC.bat" (
    call "%~dp0CONNECT_THIS_PC.bat" %*
    exit /b %errorlevel%
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0nunes_fleet_agent.ps1"
exit /b %errorlevel%
