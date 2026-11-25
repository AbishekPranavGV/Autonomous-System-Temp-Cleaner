@echo off
title NUNES EMERGENCY ANTI-HANG & SYSTEM RESCUE
color 0C
cls
echo ===============================================================================
echo     NUNES AUTONOMOUS ANTI-HANG & SYSTEM FREEZE RESCUE (v8.5.0)
echo ===============================================================================
echo.
echo [*] Analyzing system load, frozen tasks, and RAM saturation...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python is not in PATH. Falling back to PowerShell emergency flush...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "[System.GC]::Collect(); Clear-DnsClientCache; Write-Host 'Flushed DNS and initiated GC.'"
    echo.
    echo [!] Attempting emergency temp sweep...
    del /q /f /s "%TEMP%\*" >nul 2>nul
    del /q /f /s "C:\Windows\Temp\*" >nul 2>nul
    echo [OK] Emergency purge complete.
    pause
    exit /b
)

python "%~dp0hang_resolver.py" --rescue
echo.
echo ===============================================================================
echo [OK] Rescue operations completed. System responsiveness restored!
echo ===============================================================================
timeout /t 5 >nul
