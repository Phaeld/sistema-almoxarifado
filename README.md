# Sistema de Almoxarifado Interno

Aplicação desktop em Python para gestão de almoxarifado interno, com módulos de materiais, ações, abastecimento e cadastros. Interface em PySide6 (Qt) e persistência via SQLite.

## Visão Geral

O sistema organiza o fluxo do almoxarifado em módulos separados, com serviços de acesso a dados e telas independentes para cada funcionalidade.

## Funcionalidades Implementadas

- Autenticação de usuários (login)
- Sessão em memória com dados do usuário
- Tela inicial com navegação por categorias
- Consulta de ações (ACS/ACE) com filtros
- Visualização de ação em tela de solicitação (modo leitura)
- Confirmação/cancelamento de ação com persistência de status
- Atualização de estoque (entrada ACE / saída ACS)
- Tela de perfil do usuário com foto salva no banco
- Tela de ajuda
- Controle de acesso ao abastecimento por cargo (ABAST/ADMIN)
- Módulo de abastecimento:
  - Tela de controle com filtro e listagem
  - Cadastro/edição/exclusão de abastecimento
  - Cadastro/edição/exclusão de veículos
  - Detalhe do abastecimento (com foto do veículo)
  - Relatório gráfico (diário/semanal/mensal) com total, top veículo, gráfico e tabela
  - Exportação CSV/PDF com períodos (mensal/trimestral/semestral/anual)
  - Filtro adicional por mês no relatório

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
    control_gas.py
    control_gas_service.py
    vehicle_service.py
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
          ui_control_gas_window.py
          ui_control_gas_form_window.py
          ui_control_gas_vehicle_window.py
          ui_control_gas_detail_window.py
          ui_control_gas_export_window.py
          ui_control_gas_report_window.py
assets/
database/
  users.db
  material.db
  actions.db
  control.db
  vehicles.db
```

## Banco de Dados (SQLite)

- `users.db`: usuários e credenciais
- `material.db`: itens e quantidades de estoque
- `actions.db`: ações de entrada/saída (ACS/ACE) com status
- `control.db`: abastecimentos (TABLE_CONTROL_GAS)
- `vehicles.db`: cadastro de veículos (TABLE_VEHICLES)

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

## Fluxo de Ações e Estoque

1. Acesse **Consultar**
2. Filtre ações por `id_action` (ACS/ACE)
3. Dê duplo clique na ação para abrir em modo leitura
4. Em **Confirmado**, o estoque é atualizado (ACE soma, ACS subtrai)
5. Em **Cancelado**, registra status e não altera o estoque

## Fluxo de Abastecimento

1. Acesse **Abastecimento Veículos do Obras**
2. Use os filtros para listar registros
3. Duplo clique na linha para ver detalhes
4. Botões do painel:
   - Adicionar: cadastro de abastecimento
   - Editar/Excluir: atua sobre o item selecionado
   - Veículos: cadastro/edição/exclusão de veículos
5. Relatórios:
   - Impressão com resumo e gráfico
   - Exportação CSV/PDF por período

## Próximas Funcionalidades

- Validações e máscaras de data/placa
- Melhorias no layout de PDF
- Relatórios por veículo e períodos customizados
- Controle de permissões por nível de usuário
- Integração completa de colaboradores

## Autor

Raphael da Silva  
Sistema de Almoxarifado Interno
