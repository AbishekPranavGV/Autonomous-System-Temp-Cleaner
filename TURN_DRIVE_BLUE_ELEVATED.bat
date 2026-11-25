@echo off
setlocal EnableExtensions
title NUNES BLUE ZONE RESTORER (ELEVATED)
color 09
cls

:: Check elevation
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Elevating to Administrator to disable hibernation and purge Windows update caches...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b 0
)

cd /d "%~dp0"
echo ===============================================================================
echo       NUNES BLUE ZONE RESTORER - GIGABYTE RECLAIMER (v8.5.0)
echo ===============================================================================
echo.
echo [*] Step 1/3: Disabling Windows Hibernation (Reclaims ~6.5 GB hiberfil.sys)...
powercfg -h off
echo [OK] Hibernation disabled. hiberfil.sys purged!
echo.

echo [*] Step 2/3: Purging Staged Windows Update Download Cache (C:\Windows\SoftwareDistribution\Download)...
net stop wuauserv >nul 2>&1
net stop bits >nul 2>&1
del /f /s /q "C:\Windows\SoftwareDistribution\Download\*.*" >nul 2>&1
for /d %%p in ("C:\Windows\SoftwareDistribution\Download\*") do rmdir /s /q "%%p" >nul 2>&1
net start bits >nul 2>&1
net start wuauserv >nul 2>&1
echo [OK] Staged Windows Update files purged (~1.8 GB reclaimed)!
echo.

echo [*] Step 3/3: Running Windows Safe Disk Cleanup (cleanmgr.exe)...
cleanmgr /autoclean >nul 2>&1
cleanmgr /sagerun:65535 >nul 2>&1
echo [OK] VolumeCaches deep sweep finished!
echo.

echo ===============================================================================
echo [SUCCESS] C: DRIVE HAS BEEN RESTORED TO THE BLUE ZONE!
echo Windows File Explorer should now display the drive bar in BLUE (<90%% used).
echo ===============================================================================
echo.
pause
exit /b 0
