@echo off
setlocal EnableExtensions
title Autonomous System Temp Cleaner - Uninstall Daemon
color 0C

net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

schtasks /delete /tn "NunesFleetCleaner_4H_Automation" /f >nul 2>&1
schtasks /delete /tn "NunesFleetCleaner_Startup" /f >nul 2>&1
schtasks /delete /tn "NunesFleetCleaner_1H_Sentry" /f >nul 2>&1
schtasks /delete /tn "NunesFleetCleaner_4H" /f >nul 2>&1
schtasks /delete /tn "NUNES System Temp Cleaner - 4H Automation" /f >nul 2>&1

echo.
echo ========================================================
echo  Autonomous System Temp Cleaner Service Removed
echo ========================================================
echo.
echo All scheduled fleet automation tasks have been unregistered.
echo.
pause
exit /b 0
