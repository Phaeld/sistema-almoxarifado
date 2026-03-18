Param(
    [switch]$SkipApi = $false,
    [switch]$SkipClient = $false
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$pyinstaller = Join-Path $root ".venv\Scripts\pyinstaller.exe"
if (-not (Test-Path $pyinstaller)) {
    throw "PyInstaller nao encontrado em .venv\Scripts\pyinstaller.exe"
}

Write-Host "Limpando builds antigos..."
Remove-Item -Recurse -Force "$root\build" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$root\dist\Almoxarifado" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$root\dist\AlmoxAPI" -ErrorAction SilentlyContinue

if (-not $SkipClient) {
    Write-Host "Gerando executavel CLIENTE..."
    & $pyinstaller `
        --noconfirm `
        --clean `
        --onedir `
        --windowed `
        --name Almoxarifado `
        --paths "$root\src\app" `
        "$root\src\app\main.py"

    New-Item -ItemType Directory -Force "$root\dist\Almoxarifado\database" | Out-Null
    Copy-Item "$root\database\*.db" "$root\dist\Almoxarifado\database\" -Force
    if (Test-Path "$root\assets") {
        Copy-Item "$root\assets" "$root\dist\Almoxarifado\" -Recurse -Force
    }

    @"
@echo off
cd /d %~dp0
start "" ".\Almoxarifado.exe"
"@ | Set-Content "$root\dist\Almoxarifado\start_client.bat" -Encoding ASCII
}

if (-not $SkipApi) {
    Write-Host "Gerando executavel API..."
    & $pyinstaller `
        --noconfirm `
        --clean `
        --onedir `
        --console `
        --name AlmoxAPI `
        --paths "$root" `
        "$root\src\api\__main__.py"

    New-Item -ItemType Directory -Force "$root\dist\AlmoxAPI\database" | Out-Null
    Copy-Item "$root\database\*.db" "$root\dist\AlmoxAPI\database\" -Force

    @"
@echo off
cd /d %~dp0
if "%ALMOX_API_PORT%"=="" set ALMOX_API_PORT=8000
if "%ALMOX_API_HOST%"=="" set ALMOX_API_HOST=0.0.0.0
start "" ".\AlmoxAPI.exe"
"@ | Set-Content "$root\dist\AlmoxAPI\start_api.bat" -Encoding ASCII
}

Write-Host ""
Write-Host "Build concluido."
Write-Host "Cliente: $root\dist\Almoxarifado"
Write-Host "API:     $root\dist\AlmoxAPI"

