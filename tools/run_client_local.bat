@echo off
cd /d %~dp0\..
if "%ALMOX_API_BASE_URL%"=="" set ALMOX_API_BASE_URL=http://127.0.0.1:8000
if "%ALMOX_API_KEY%"=="" set ALMOX_API_KEY=SysObras-2026
python src\app\main.py

