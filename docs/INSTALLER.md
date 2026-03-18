# Gerar Executavel e Instalador

## 1) Preparar ambiente

```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
```

## 2) Gerar executaveis (cliente + API)

```powershell
powershell -ExecutionPolicy Bypass -File tools\build_release.ps1
```

Saida:

- `dist\Almoxarifado\Almoxarifado.exe`
- `dist\AlmoxAPI\AlmoxAPI.exe`

## 3) Gerar instalador (.exe)

Instale o Inno Setup e rode:

```powershell
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\AlmoxarifadoSuite.iss
```

Saida:

- `dist\installer\AlmoxarifadoSuite-Setup.exe`
- Instalador cria atalhos:
  - `Almoxarifado Obras`
  - `Almoxarifado API`
  - `Almoxarifado Completo (API+App)`

## 4) Teste rapido em 1 maquina

Abrir API:

```powershell
tools\run_server_local.bat
```

Abrir cliente:

```powershell
tools\run_client_local.bat
```

## 5) Teste em outra maquina

No cliente, definir antes de abrir:

```powershell
set ALMOX_API_BASE_URL=http://IP_DA_MAQUINA_SERVIDOR:8000
set ALMOX_API_KEY=SysObras-2026
```
