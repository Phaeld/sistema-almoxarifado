# 📦 Sistema de Almoxarifado Interno

Sistema desktop desenvolvido em **Python** para gerenciamento de almoxarifado interno, com controle de usuários, sessões, perfis e, futuramente, estoque, entradas, saídas e relatórios.

O projeto utiliza **PySide6 (Qt)** para a interface gráfica e segue uma arquitetura organizada por módulos, facilitando manutenção e evolução.

---

## 🚀 Funcionalidades Implementadas

### 🔐 Autenticação
- Login de usuários via `auth_service.py`
- Validação de credenciais
- Bloqueio de acesso sem autenticação

### 🧠 Sessão de Usuário
- Gerenciamento centralizado de sessão (`Session`)
- Dados do usuário disponíveis em todas as telas
- Sessão mantida enquanto o usuário estiver logado
- Encerramento da sessão apenas ao clicar em **Sair**

### 👤 Perfil do Usuário
- Tela de perfil com:
  - Usuário
  - Nome
  - Cargo
  - Nível de acesso (convertido de valor numérico para texto)
  - Foto de perfil vinculada ao banco de dados
- Foto padrão quando o usuário não possui imagem cadastrada
- Estrutura pronta para:
  - Alterar foto
  - Remover foto

### 🧭 Navegação
- Botão **Inicial** para retornar à Home
- Botão **Sair** encerra a sessão e retorna ao login
- Proteção de rotas: telas não abrem sem sessão ativa

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **PySide6 (Qt for Python)**
- **Arquitetura modular**
- **Orientação a Objetos**
- **Dicionário de sessão em memória**
- **Integração com banco de dados (em andamento)**

---

## 📂 Estrutura do Projeto

```text
src/
├── app/
│   ├── home.py
│   ├── profile.py
│   ├── main.py
|   ├── screen_filter.py
|   └── help.py
│
├── auth/
│   ├── auth_service.py
│   └── session.py
│
├── gui/
│   └── window/
│       └── main_window/
│           └── ui_profile_window.py
|           └── ui_main_window.py
|           └── ui_home_window.py
|           └── ui_screen_filter_window.py
|           └── ui_help_window.py
│
├── assets/
│   ├── icon.jpg
│   ├── home.png
│   ├── exit.png
│   └── user_profile.png
│
└── main.py
```

## 🧩 Sessão de Usuário (Resumo Técnico)

A sessão é gerenciada pelo arquivo:
```
auth/session.py
```
<br>

### Ela armazena:

ID do usuário

Username

Nome

Cargo

Nível de acesso

Caminho da foto de perfil

### A sessão:

É criada após login bem-sucedido

Pode ser acessada por qualquer tela

É encerrada apenas via logout

## 📸 Foto de Perfil

O caminho da foto é carregado a partir do banco de dados
Caso o arquivo exista, ele é exibido
Caso contrário, uma imagem padrão é utilizada
Imagem exibida em formato circular

## 🔒 Segurança

Telas protegidas por verificação de sessão

Usuário não autenticado não acessa Home ou Perfil

Logout limpa completamente os dados da sessão

## 🔮 Próximos Passos

Cadastro e gerenciamento de produtos

Controle de entrada e saída de materiais

Relatórios em PDF

Controle de permissões por nível de usuário

Persistência completa via banco de dados

Upload de foto de perfil diretamente pela interface

## 👨‍💻 Autor

Raphael da Silva

Sistema desenvolvido para gerenciamento interno de almoxarifado.

Projeto em constante evolução 🚀