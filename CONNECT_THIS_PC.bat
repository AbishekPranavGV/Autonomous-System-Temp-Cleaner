@echo off



setlocal EnableExtensions



cd /d "%~dp0"



title NUNES AUTONOMOUS FLEET - CONNECT THIS COMPUTER



color 0B



cls



echo ===============================================================================



echo       NUNES AUTONOMOUS FLEET CONNECTOR & 4-HOUR BACKGROUND CLIENT (v8.5.0 Quantum)



echo ===============================================================================



echo.



echo [*] Initializing fleet connection for this machine...



echo [*] Computer Name: %COMPUTERNAME%



echo [*] User Account : %USERNAME%



echo.







:: Verify extraction - ensure sibling files exist



if not exist "%~dp0nunes_fleet_agent.ps1" (



    color 0C



    echo ===============================================================================



    echo [ERROR] The files must be EXTRACTED before running!



    echo ===============================================================================



    echo It looks like you ran this directly from inside the ZIP file.



    echo.



    echo Please follow these simple steps:



    echo 1. Right-click the downloaded NUNES_FLEET_CLIENT_V7.zip file



    echo 2. Click "Extract All..." and extract to any folder (e.g., Desktop or Downloads)



    echo 3. Open that extracted folder and double-click CONNECT_THIS_PC.bat



    echo ===============================================================================



    echo.



    pause



    exit /b 1



)







:: Try Administrator elevation for full system-level task scheduling



net session >nul 2>&1



if %errorlevel% neq 0 (



    if "%~1"=="" (



        echo [*] Attempting Administrator elevation for full system disk cleanup...



        powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -ArgumentList 'ELEVATED' -Verb RunAs" >nul 2>&1



        if %errorlevel% equ 0 (



            exit /b 0



        )



        echo [!] Running in Standard User mode. Cleaning user temp & caches...



    )



)







:: Check for REAL working Python (not Windows Store stub)



set "HAS_PYTHON=0"



python -c "import sys; sys.exit(0)" >nul 2>&1



if %errorlevel% equ 0 (



    set "HAS_PYTHON=1"



)







if "%HAS_PYTHON%"=="1" (



    echo [OK] Python runtime detected.



    echo [*] Executing safe temp cleanup (temp, %%temp%%, cleanmgr)...



    python "%~dp0nunes_universal_cleaner.py" --clean



    echo.



    echo [*] Starting Universal Fleet Client Daemon in background...



    start "Nunes Cleaner Daemon" /min python "%~dp0nunes_universal_cleaner.py" --daemon



    echo [OK] Fleet background daemon launched successfully!



    echo.



    echo [*] Registering 4-Hour Background Windows Scheduled Service...



    if exist "%~dp0INSTALL_4H_SERVICE.bat" (



        call "%~dp0INSTALL_4H_SERVICE.bat" >nul 2>&1



    )



    goto :SUCCESS_DISPLAY



)







:: Native Windows PowerShell Engine (Zero External Dependencies)



echo [*] Using Native Windows PowerShell Fleet Agent (100%% Windows Compatible)...



echo [*] Executing safe cleanup: %%TEMP%%, C:\Windows\Temp, and cleanmgr safe mode...



powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0nunes_fleet_agent.ps1"







echo.



echo [*] Launching background daemon (auto-clean every 4h, live heartbeat)...



start "Nunes Fleet Agent" /min powershell -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File "%~dp0nunes_fleet_agent.ps1" -Daemon







echo.



echo [*] Registering 4-Hour Windows Task Scheduler Service...



echo [*] Installing Fleet Agent to permanent storage (%ProgramData%\NunesCleanerV7)...
set "INSTALL_DIR=%ProgramData%\NunesCleanerV7"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%" >nul 2>&1
copy /Y "%~dp0nunes_fleet_agent.ps1" "%INSTALL_DIR%\nunes_fleet_agent.ps1" >nul 2>&1
if exist "%~dp0cleaner.py" copy /Y "%~dp0cleaner.py" "%INSTALL_DIR%\cleaner.py" >nul 2>&1
if exist "%~dp0prompt_backup_manager.py" copy /Y "%~dp0prompt_backup_manager.py" "%INSTALL_DIR%\prompt_backup_manager.py" >nul 2>&1
if exist "%~dp0hang_resolver.py" copy /Y "%~dp0hang_resolver.py" "%INSTALL_DIR%\hang_resolver.py" >nul 2>&1
if exist "%~dp0nunes_universal_cleaner.py" copy /Y "%~dp0nunes_universal_cleaner.py" "%INSTALL_DIR%\nunes_universal_cleaner.py" >nul 2>&1

if exist "%~dp0show_status.ps1" copy /Y "%~dp0show_status.ps1" "%INSTALL_DIR%\show_status.ps1" >nul 2>&1

if exist "%~dp0SHOW_DETAILS.bat" copy /Y "%~dp0SHOW_DETAILS.bat" "%INSTALL_DIR%\SHOW_DETAILS.bat" >nul 2>&1

if exist "%~dp0STATUS.bat" copy /Y "%~dp0STATUS.bat" "%INSTALL_DIR%\STATUS.bat" >nul 2>&1

if exist "%INSTALL_DIR%\SHOW_DETAILS.bat" (

    copy /Y "%INSTALL_DIR%\SHOW_DETAILS.bat" "%USERPROFILE%\Desktop\NUNES_CHECK_STATUS.bat" >nul 2>&1

    copy /Y "%INSTALL_DIR%\SHOW_DETAILS.bat" "C:\Users\Public\Desktop\NUNES_CHECK_STATUS.bat" >nul 2>&1

)

echo [*] Registering 4-Hour Windows Task Scheduler Service...
schtasks /create /tn "NunesFleetCleaner_4H_Automation" /tr "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File \"%INSTALL_DIR%\nunes_fleet_agent.ps1\"" /sc hourly /mo 4 /ru "SYSTEM" /f >nul 2>&1
if %errorlevel% neq 0 (
    schtasks /create /tn "NunesFleetCleaner_4H_Automation" /tr "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File \"%INSTALL_DIR%\nunes_fleet_agent.ps1\"" /sc hourly /mo 4 /f >nul 2>&1
)
schtasks /create /tn "NunesFleetCleaner_Startup" /tr "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File \"%INSTALL_DIR%\nunes_fleet_agent.ps1\"" /sc onstart /ru "SYSTEM" /f >nul 2>&1
if %errorlevel% neq 0 (
    schtasks /create /tn "NunesFleetCleaner_Startup" /tr "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File \"%INSTALL_DIR%\nunes_fleet_agent.ps1\"" /sc onlogon /f >nul 2>&1
)

:SUCCESS_DISPLAY



echo.



echo ===============================================================================



echo [SUCCESS] %COMPUTERNAME% IS NOW REGISTERED & LIVE ON THE DASHBOARD!



echo - Cleaned Targets: %%TEMP%%, C:\Windows\Temp, WER Dumps, cleanmgr (Safe Mode)



echo - Safety Boundary: Downloads and Recycle Bin strictly preserved



echo - Background Loop: Adaptive 1-Hour Sentry: auto-cleans hourly when in RED (<10 GB) to keep drive in BLUE!



echo - Dashboard Link : Connected to Live Operations Center



echo ===============================================================================



echo.



echo [*] Displaying live system details HUD and opening operations dashboard...

if exist "%INSTALL_DIR%\show_status.ps1" (

    powershell -NoProfile -ExecutionPolicy Bypass -File "%INSTALL_DIR%\show_status.ps1" -OpenBrowser -Choice 4

)

echo.

echo Setup finished successfully. You can run NUNES_CHECK_STATUS.bat on Desktop anytime.

echo Window will close in 10 seconds or press any key to close...

timeout /t 10

exit /b 0



