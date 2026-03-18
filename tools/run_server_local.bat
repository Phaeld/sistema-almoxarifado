@echo off
cd /d %~dp0\..
set ALMOX_API_HOST=0.0.0.0
set ALMOX_API_PORT=8000
if "%ALMOX_API_KEY%"=="" set ALMOX_API_KEY=SysObras-2026
python -m src.api

