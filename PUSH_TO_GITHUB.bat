@echo off
title NUNES TEMP CLEANER - PUSH LIVE TO GITHUB
color 0A
cls
cd /d "d:\Downloads\Autonomous-System-Temp-Cleaner"

echo ===============================================================================
echo     NUNES AUTONOMOUS FLEET TEMP CLEANER - LIVE GITHUB SYNCHRONIZER
echo ===============================================================================
echo Repository: %CD%
echo.
echo [*] Dynamically rebuilding client ZIP package with latest scripts...
python zip_builder.py
echo.
echo [*] Checking git status...
git status -s
echo.
echo [*] Staging all updates (Dynamic Zip Builder, Live Files Inspector, Light Theme UI)...
git add .
echo.
echo [*] Committing changes...
git commit -m "feat(zip): real-time dynamic zip builder, always-updated client package, and auto-sync" 2>nul
echo.
echo [*] Pushing live to GitHub origin main...
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo ===============================================================================
    echo [SUCCESS] PUSHED LIVE TO GITHUB!
    echo Your GitHub Pages (github.io) and Vercel will update automatically!
    echo Repository: https://github.com/AbishekPranavGV/Autonomous-System-Temp-Cleaner
    echo ===============================================================================
) else (
    echo ===============================================================================
    echo [!] Push failed or requires authorization.
    echo If GitHub Credential Manager prompt opened in your browser, please approve it.
    echo ===============================================================================
)
echo.
pause
