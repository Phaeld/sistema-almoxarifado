# 📦 Sistema de Gestão de Almoxarifado Interno

Sistema desktop desenvolvido para gerenciamento de almoxarifado interno da Secretaria municipal de Obras, permitindo o controle de materiais, funcionários, permissões, retiradas, relatórios e documentação do sistema de forma centralizada, intuitiva e segura.

---

## 📌 Visão Geral

O **Sistema de Gestão de Almoxarifado Interno** foi projetado para atender empresas que necessitam controlar materiais de uso interno, garantindo rastreabilidade, organização e facilidade de operação.

A aplicação é desenvolvida em **Python**, com interface gráfica moderna utilizando **Qt (PySide6)**, seguindo boas práticas de organização de código, escalabilidade e experiência do usuário.

---

## 🎯 Objetivos do Projeto

- Centralizar o controle de materiais e ferramentas
- Reduzir erros manuais e perdas de estoque
- Garantir rastreabilidade de retiradas e devoluções
- Facilitar auditorias e geração de relatórios
- Oferecer uma interface clara, moderna e responsiva

---

## 🛠️ Tecnologias Utilizadas

### 🔹 Linguagem
- **Python 3.12+**

### 🔹 Interface Gráfica (GUI)
- **Qt / PySide6**
- Layouts responsivos com `QVBoxLayout`, `QHBoxLayout`
- Componentes personalizados (cards, Q&A expansível)
- `QScrollArea` para navegação em telas extensas
- Estilização via **Qt Stylesheets (QSS)**

### 🔹 Arquitetura
- Organização modular por camadas:
  - `app/`
  - `gui/`
  - `window/`
- Separação entre lógica, interface e recursos
- Estrutura preparada para crescimento do sistema

### 🔹 Recursos Visuais
- Ícones e imagens em PNG
- Gerenciamento de assets via `resources_rc`
- Identidade visual consistente (cores, tipografia)

---

## 📄 Funcionalidades Desenvolvidas Até o Momento

### ✅ Estrutura Base do Sistema
- Inicialização da aplicação
- Janela principal configurada
- Barra superior de navegação (Home / Perfil)
- Telas de login(main.py), inicial(home.py), filtro tabelas(screen_filter.py) e a ajuda(help.py)

### ✅ Tela de Ajuda (Help)
- Layout inspirado em interface profissional
- Seções explicativas do sistema
- Manual de uso integrado
- Botão para download de manual em PDF (estrutura pronta)
- Sistema de **Q&A (Perguntas e Respostas)** com:
  - Cards expansíveis
  - Interação via clique
  - Organização visual clara
- Scroll vertical para conteúdos extensos

### ✅ Componentes Reutilizáveis
- Títulos de seção padronizados
- Parágrafos com destaque
- Componentes interativos customizados (Accordion/Q&A)

---

## 🧱 Estrutura Atual do Projeto

sistema-almoxarifado/<br>
│<br>
├── assets/ # Imagens, ícones e recursos visuais<br>
├── src/<br>
│ └── app/<br>
│ ├── gui/<br>
│ │ └── window/<br>
│ │ └── main_window/<br>
│ │ └── ui_main_window.py<br>
│ │ └── ui_home_window.py<br>
│ │ └── ui_help_window.py<br>
│ │ └── ui_screen_filter_window.py<br>
│ ├── home.py<br>
│ ├── main.py<br>
│ └── qt_core.py<br>
│<br>
├── .venv/ # Ambiente virtual Python<br>
├── README.md<br>
├── LICENSE<br>
└── .gitignore<br>



---

## 🔜 Tecnologias e Funcionalidades Planejadas

### 🗄️ Banco de Dados
- **SQLite**
  - Armazenamento local de:
    - Produtos
    - Funcionários
    - Movimentações de estoque
    - Logs do sistema
  - Estrutura preparada para futura migração (ex: PostgreSQL)

### 📊 Relatórios
- Geração de relatórios por período
- Exportação de dados
- Filtros por material, usuário e tipo de movimentação

### 🖨️ Impressão e PDF
- API interna para:
  - Impressão direta
  - Exportação de relatórios em **PDF**
- Possível integração com:
  - `ReportLab`
  - `QtPrintSupport`
  - `WeasyPrint` ou similares

### 📝 Sistema de Logs
- Registro automático de:
  - Acessos
  - Alterações
  - Retiradas e devoluções
- Logs organizados por data e usuário
- Base para auditoria e rastreabilidade

### 🔐 Controle de Permissões
- Níveis de acesso por usuário
- Restrições por função (admin, operador, visualização)
- Integração com a tela "Meu Perfil"

---

## 🚀 Status do Projeto

📍 **Em desenvolvimento ativo**  
📅 Início: 2025  
👤 Autor: **Raphael da Silva**

O projeto encontra-se em fase de construção da interface e estrutura base, com foco em usabilidade, organização e preparação para integração com banco de dados e serviços.

---

## 📌 Próximos Passos Imediatos

- Implementação do SQLite
- Criação dos modelos de dados
- Sistema de cadastro (CRUD)
- Integração dos relatórios
- Implementação do sistema de logs
- Exportação e impressão em PDF

---

## 📜 Licença

Este projeto está licenciado sob os termos definidos no arquivo [LICENSE](LICENSE).