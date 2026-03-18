; Inno Setup script
; Gere os executaveis antes: powershell -ExecutionPolicy Bypass -File tools\build_release.ps1

#define MyAppName "Almoxarifado Obras"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Raphael da Silva"
#define MyAppURL "https://example.local"
#define MyAppExeName "Almoxarifado.exe"
#define MyApiExeName "AlmoxAPI.exe"

[Setup]
AppId={{6F25D0B8-2DAA-4E2E-9629-EA3A95F3A122}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\AlmoxarifadoObras
DefaultGroupName={#MyAppName}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
OutputDir=dist\installer
OutputBaseFilename=AlmoxarifadoSuite-Setup

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "dist\Almoxarifado\*"; DestDir: "{app}\Almoxarifado"; Flags: recursesubdirs createallsubdirs
Source: "dist\AlmoxAPI\*"; DestDir: "{app}\AlmoxAPI"; Flags: recursesubdirs createallsubdirs
Source: "installer\start_suite.bat"; DestDir: "{app}"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na area de trabalho"; GroupDescription: "Atalhos:"; Flags: unchecked
Name: "startmenuicon"; Description: "Criar atalhos no Menu Iniciar"; GroupDescription: "Atalhos:"; Flags: checkedonce

[Icons]
Name: "{autodesktop}\Almoxarifado Obras"; Filename: "{app}\Almoxarifado\{#MyAppExeName}"; Tasks: desktopicon
Name: "{autodesktop}\Almoxarifado API"; Filename: "{app}\AlmoxAPI\{#MyApiExeName}"; Tasks: desktopicon
Name: "{autodesktop}\Almoxarifado Completo (API+App)"; Filename: "{app}\start_suite.bat"; Tasks: desktopicon
Name: "{group}\Almoxarifado Obras"; Filename: "{app}\Almoxarifado\{#MyAppExeName}"; Tasks: startmenuicon
Name: "{group}\Almoxarifado API"; Filename: "{app}\AlmoxAPI\{#MyApiExeName}"; Tasks: startmenuicon
Name: "{group}\Almoxarifado Completo (API+App)"; Filename: "{app}\start_suite.bat"; Tasks: startmenuicon

[Run]
Filename: "{app}\AlmoxAPI\{#MyApiExeName}"; Description: "Executar API agora"; Flags: postinstall skipifsilent
Filename: "{app}\Almoxarifado\{#MyAppExeName}"; Description: "Abrir sistema agora"; Flags: postinstall skipifsilent
