@echo off
setlocal
title NUNES Cleaner Dashboard

set "SCRIPT_DIR=%~dp0"
set "DASHBOARD_APP=%SCRIPT_DIR%dashboard\app.py"

echo ========================================================
echo    NUNES FLEET CLEANER - LIVE DASHBOARD LAUNCHER
echo ========================================================
echo.
echo Starting dashboard server on port 8090...

powershell -NoProfile -Command "Start-Process python -ArgumentList @('%DASHBOARD_APP%') -WindowStyle Minimized"

ping 127.0.0.1 -n 3 >nul

echo Opening live dashboard in your default browser...
start "" "http://localhost:8090"

echo.
echo Dashboard is running live!
echo Local Address : http://localhost:8090
echo Cloud Address : https://nunes-temp-cleaner-dashboard.vercel.app
echo.
ping 127.0.0.1 -n 4 >nul
exit /b 0
