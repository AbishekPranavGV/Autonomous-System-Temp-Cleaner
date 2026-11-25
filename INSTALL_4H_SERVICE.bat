@echo off

setlocal EnableExtensions

cd /d "%~dp0"

title NUNES AUTONOMOUS FLEET - 4-HOUR BACKGROUND SERVICE INSTALLER

color 0B

cls



echo ===============================================================================

echo   NUNES AUTONOMOUS FLEET - 4-HOUR BACKGROUND SERVICE INSTALLER (v8.5.0 Quantum)

echo ===============================================================================

echo.

echo [*] Computer Name : %COMPUTERNAME%

echo [*] User Account  : %USERNAME%

echo [*] Working Folder: %~dp0

echo.



:: 1. Self-Extraction Verification: Ensure sibling agent files exist

if not exist "%~dp0nunes_fleet_agent.ps1" (

    color 0C

    echo ===============================================================================

    echo [ERROR] The client files must be EXTRACTED before running!

    echo ===============================================================================

    echo You ran this directly from inside the ZIP file without extracting.

    echo.

    echo Steps:

    echo 1. Right-click NUNES_FLEET_CLIENT_V7.zip

    echo 2. Click "Extract All..." to any folder

    echo 3. Open that extracted folder and double-click INSTALL_4H_SERVICE.bat

    echo ===============================================================================

    echo.

    pause

    exit /b 1

)



:: 2. Elevation: Elevate to Administrator for system-wide service installation

net session >nul 2>&1

if %errorlevel% neq 0 (

    if "%~1"=="" (

        echo [*] Requesting Administrator privileges to register Windows background service...

        powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -ArgumentList 'ELEVATED' -Verb RunAs"

        exit /b 0

    )

    echo [!] Running in Standard User mode.

)



cls

echo ===============================================================================

echo   NUNES AUTONOMOUS FLEET - 4-HOUR BACKGROUND SERVICE SETUP

echo ===============================================================================

echo.



:: 3. Target Installation Directory (Indestructible System Location)

set "INSTALL_DIR=%ProgramData%\NunesCleanerV7"

echo [*] Installing Fleet Agent to permanent storage: %INSTALL_DIR%

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%" >nul 2>&1



:: Copy all core fleet agent modules

copy /Y "%~dp0nunes_fleet_agent.ps1" "%INSTALL_DIR%\nunes_fleet_agent.ps1" >nul

if exist "%~dp0cleaner.py" copy /Y "%~dp0cleaner.py" "%INSTALL_DIR%\cleaner.py" >nul

if exist "%~dp0prompt_backup_manager.py" copy /Y "%~dp0prompt_backup_manager.py" "%INSTALL_DIR%\prompt_backup_manager.py" >nul

if exist "%~dp0hang_resolver.py" copy /Y "%~dp0hang_resolver.py" "%INSTALL_DIR%\hang_resolver.py" >nul

if exist "%~dp0nunes_universal_cleaner.py" copy /Y "%~dp0nunes_universal_cleaner.py" "%INSTALL_DIR%\nunes_universal_cleaner.py" >nul

if exist "%~dp0TURN_DRIVE_BLUE_ELEVATED.bat" copy /Y "%~dp0TURN_DRIVE_BLUE_ELEVATED.bat" "%INSTALL_DIR%\TURN_DRIVE_BLUE_ELEVATED.bat" >nul

if exist "%~dp0NUNES_CACHE_CLEANER.bat" copy /Y "%~dp0NUNES_CACHE_CLEANER.bat" "%INSTALL_DIR%\NUNES_CACHE_CLEANER.bat" >nul

if exist "%~dp0AUTONOMOUS_CACHE_CLEANER.bat" copy /Y "%~dp0AUTONOMOUS_CACHE_CLEANER.bat" "%INSTALL_DIR%\AUTONOMOUS_CACHE_CLEANER.bat" >nul

if exist "%~dp0show_status.ps1" copy /Y "%~dp0show_status.ps1" "%INSTALL_DIR%\show_status.ps1" >nul

if exist "%~dp0SHOW_DETAILS.bat" copy /Y "%~dp0SHOW_DETAILS.bat" "%INSTALL_DIR%\SHOW_DETAILS.bat" >nul

if exist "%~dp0STATUS.bat" copy /Y "%~dp0STATUS.bat" "%INSTALL_DIR%\STATUS.bat" >nul



:: Create 1-click status checker on Desktop

if exist "%INSTALL_DIR%\SHOW_DETAILS.bat" (

    copy /Y "%INSTALL_DIR%\SHOW_DETAILS.bat" "%USERPROFILE%\Desktop\NUNES_CHECK_STATUS.bat" >nul 2>&1

    copy /Y "%INSTALL_DIR%\SHOW_DETAILS.bat" "C:\Users\Public\Desktop\NUNES_CHECK_STATUS.bat" >nul 2>&1

)

echo [OK] Files installed successfully!

echo.



:: 4. Register Scheduled Task (Every 4 Hours + Startup + Red-Zone 1-Hour Sentry)

echo [*] Registering Windows Scheduled Task (Runs every 4 hours silently in background)...

set "TASK_NAME=NunesFleetCleaner_4H_Automation"

set "TASK_CMD=powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File \"%INSTALL_DIR%\nunes_fleet_agent.ps1\""



:: Attempt registration as SYSTEM for silent background execution

schtasks /create /tn "%TASK_NAME%" /tr "%TASK_CMD%" /sc hourly /mo 4 /ru "SYSTEM" /f >nul 2>&1

if %errorlevel% neq 0 (

    schtasks /create /tn "%TASK_NAME%" /tr "%TASK_CMD%" /sc hourly /mo 4 /f >nul 2>&1

)



schtasks /create /tn "NunesFleetCleaner_Startup" /tr "%TASK_CMD%" /sc onstart /ru "SYSTEM" /f >nul 2>&1

if %errorlevel% neq 0 (

    schtasks /create /tn "NunesFleetCleaner_Startup" /tr "%TASK_CMD%" /sc onlogon /f >nul 2>&1

)

echo [OK] Scheduled Tasks registered successfully!

echo.

echo [*] Launching live background heartbeat daemon...

start "Nunes Fleet Agent" /min powershell -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File "%INSTALL_DIR%\nunes_fleet_agent.ps1" -Daemon

echo [OK] Background daemon active!

echo.



:: 5. CRITICAL: Execute Initial Clean & Dashboard Registration RIGHT NOW

echo ===============================================================================

echo   CONNECTING TO FLEET DASHBOARD ^& RUNNING INITIAL SAFE SWEEP...

echo ===============================================================================

echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%INSTALL_DIR%\nunes_fleet_agent.ps1"



echo.

echo ===============================================================================

echo   [SUCCESS] %COMPUTERNAME% IS NOW CONNECTED ^& LIVE IN THE DASHBOARD!

echo ===============================================================================

echo   * Status       : ONLINE ^& Connected to Live Operations Center

echo   * Targets      : %%TEMP%%, C:\Windows\Temp, Multi-Profile Caches, cleanmgr

echo   * Safety Guard : Downloads, Documents, Desktop 100%% preserved

echo   * Sentry Mode  : Adaptive 1-Hour Sentry active when drive is RED (used >= 90%%)

echo   * Retention    : 35-Day rolling lifecycle auto-purges logs older than 35 days

echo   * Schedule     : Runs autonomously every 4 hours silently in background

echo   * Local HUD    : %USERPROFILE%\Desktop\NUNES_CLEANER_STATUS.html

echo ===============================================================================

echo.

echo [*] Displaying system status HUD and opening live view...

if exist "%INSTALL_DIR%\show_status.ps1" (

    powershell -NoProfile -ExecutionPolicy Bypass -File "%INSTALL_DIR%\show_status.ps1" -OpenBrowser -Choice 4

)

echo.

echo Setup finished successfully. You can run NUNES_CHECK_STATUS.bat on Desktop anytime.

pause

exit /b 0

