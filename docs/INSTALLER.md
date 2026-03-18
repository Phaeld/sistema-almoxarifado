# Instalacao, Execucao e Exportacao

## 1. Abrir o sistema na maquina de desenvolvimento sem usar `main.py`

Agora voce pode abrir o sistema por arquivo `.bat`, sem rodar o comando manual do Python.

Arquivos disponiveis na raiz do projeto:

- `abrir_sistema_local.bat`
- `abrir_api_local.bat`
- `abrir_sistema_completo_local.bat`

Uso:

- abrir somente o cliente:
  - duplo clique em `abrir_sistema_local.bat`
- abrir somente a API:
  - duplo clique em `abrir_api_local.bat`
- abrir API + cliente:
  - duplo clique em `abrir_sistema_completo_local.bat`

Observacao:

- esses arquivos usam o Python da `.venv`
- se a `.venv` nao existir, o script para e mostra erro

---

## 2. Gerar executaveis

### 2.1 Preparar ambiente

```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
```

### 2.2 Build

```powershell
powershell -ExecutionPolicy Bypass -File tools\build_release.ps1
```

Saida esperada:

- `dist\Almoxarifado\`
- `dist\AlmoxAPI\`

Arquivos principais gerados:

- `dist\Almoxarifado\Almoxarifado.exe`
- `dist\Almoxarifado\start_client.bat`
- `dist\Almoxarifado\assets\...`
- `dist\Almoxarifado\database\...`
- `dist\AlmoxAPI\AlmoxAPI.exe`
- `dist\AlmoxAPI\start_api.bat`
- `dist\AlmoxAPI\database\...`

Importante:

- nao copie apenas o `.exe`
- o executavel depende da pasta ao redor
- sempre leve a pasta inteira `dist\Almoxarifado` ou `dist\AlmoxAPI`

---

## 3. Teste local apos o build

### 3.1 Testar API

```powershell
dist\AlmoxAPI\start_api.bat
```

### 3.2 Testar cliente

```powershell
dist\Almoxarifado\start_client.bat
```

### 3.3 Testar os dois

1. abrir `dist\AlmoxAPI\start_api.bat`
2. depois abrir `dist\Almoxarifado\start_client.bat`

---

## 4. Gerar instalador

### 4.1 Requisito

Instalar o Inno Setup 6.

### 4.2 Comando

```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "installer\AlmoxarifadoSuite.iss"
```

Saida esperada:

- `dist\installer\AlmoxarifadoSuite-Setup.exe`

---

## 5. O que o instalador cria

O instalador agora cria atalhos chamando os launchers `.bat`, nao os `.exe` crus.

Atalhos:

- `Almoxarifado Obras`
- `Almoxarifado API`
- `Almoxarifado Completo (API+App)`

Isso reduz erro de abertura por diretorio de trabalho incorreto.

---

## 6. Como instalar em outra maquina

### 6.1 Opcao 1 - teste rapido sem instalador

Copie:

- `dist\Almoxarifado`
- `dist\AlmoxAPI`

Na maquina servidor:

```powershell
dist\AlmoxAPI\start_api.bat
```

Na maquina cliente:

```powershell
set ALMOX_API_BASE_URL=http://IP_DO_SERVIDOR:8000
set ALMOX_API_KEY=SysObras-2026
dist\Almoxarifado\start_client.bat
```

### 6.2 Opcao 2 - com instalador

Copie:

- `dist\installer\AlmoxarifadoSuite-Setup.exe`

Execute na outra maquina e conclua a instalacao.

---

## 7. Motivo mais comum para o executavel nao abrir

Os motivos mais comuns sao:

- abrir somente o `Almoxarifado.exe` fora da pasta original
- faltar `assets`
- faltar `database`
- abrir cliente sem API configurada/disponivel
- atalho chamando o executavel sem o diretorio correto

Com os launchers `.bat` e o instalador apontando para eles, esse problema tende a desaparecer.
