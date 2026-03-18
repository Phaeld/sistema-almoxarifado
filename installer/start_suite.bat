@echo off
cd /d %~dp0
if "%ALMOX_API_HOST%"=="" set ALMOX_API_HOST=127.0.0.1
if "%ALMOX_API_PORT%"=="" set ALMOX_API_PORT=8000
if "%ALMOX_API_BASE_URL%"=="" set ALMOX_API_BASE_URL=http://127.0.0.1:8000
start "" ".\AlmoxAPI\AlmoxAPI.exe"
timeout /t 2 >nul
start "" ".\Almoxarifado\Almoxarifado.exe"

