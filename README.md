# Sistema de Almoxarifado Interno

Aplicação desktop em Python para gestão de almoxarifado interno, com foco em controle de materiais, solicitações, consultas e usuários. Interface construída com PySide6 (Qt) e persistência via SQLite.

## Visão Geral

O sistema organiza o fluxo do almoxarifado em módulos: autenticação, sessão, consulta de ações, filtros de materiais e perfil do usuário. A base é modular, com serviços dedicados para acesso a dados e telas independentes.

## Funcionalidades Implementadas

- Autenticação de usuários (login)
- Sessão em memória com dados do usuário
- Tela inicial com navegação por categorias
- Consulta de ações (ACS/ACE) com filtros
- Visualização de ação em tela de solicitação (modo leitura)
- Confirmação/cancelamento da ação
- Atualização de estoque ao confirmar (subtração do material)
- Tela de perfil do usuário
- Tela de ajuda

## Estrutura do Projeto

```
src/
  app/
    main.py
    home.py
    screen_filter.py
    profile.py
    help.py
    action_service.py
    material_service.py
    auth/
      auth_service.py
      session.py
    gui/
      resources.qrc
      resources_rc.py
      window/
        main_window/
          ui_main_window.py
          ui_home_window.py
          ui_screen_filter_window.py
          ui_profile_window.py
          ui_help_window.py
assets/
database/
  users.db
  material.db
  actions.db
```

## Banco de Dados (SQLite)

- `users.db`: usuários e credenciais
- `material.db`: itens e quantidades de estoque
- `actions.db`: ações de entrada/saída (ACS/ACE)

## Como Executar

1. Crie e ative um ambiente virtual
2. Instale dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute:
   ```
   python src/app/main.py
   ```

## Fluxo de Consulta e Atualização

1. Acesse **Consultar**
2. Filtre ações por `id_action` (ACS/ACE)
3. Dê duplo clique na ação para abrir em modo leitura
4. Em **Confirmado**, o estoque é atualizado (subtração)
5. Em **Cancelado**, apenas registra o cancelamento local

## Próximas Funcionalidades

- Persistência de status (confirmado/cancelado) no `actions.db`
- Vinculação de múltiplos itens por ação
- Relatórios e exportação
- Cadastro completo de colaboradores pela interface
- Entrada de materiais (ACE) com incremento de estoque
- Controle de permissões por nível de usuário

## Autor

Raphael da Silva  
Sistema de Almoxarifado Interno
