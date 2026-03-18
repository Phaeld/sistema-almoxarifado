@echo off
cd /d %~dp0
start "" cmd /k tools\run_server_local.bat
timeout /t 2 >nul
start "" cmd /k tools\run_client_local.bat
