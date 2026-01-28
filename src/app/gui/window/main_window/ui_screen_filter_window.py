"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    Internal warehouse management system with graphical interface.
====================================================================
"""

# IMPORT QT CORE
from qt_core import *

# IMPORT RESOURCES
from gui import resources_rc


class UI_ScreenFilterWindow(object):

    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("ScreenFilterWindow")

        # WINDOW SETTINGS
        parent.resize(1200, 720)
        parent.setMinimumSize(960, 540)
        parent.setWindowTitle("Almoxarifado Obras - Filtros, Pedidos e Consultas")
        parent.setWindowIcon(QIcon(":/assets/icon.jpg"))
        parent.setStyleSheet("background-color: #E8E2EE;")

        # CENTRAL WIDGET
        self.central_widget = QWidget(parent)
        parent.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =============================
        # TOP BAR
        # =============================
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(50)
        self.top_bar.setStyleSheet("background-color: #390E68;")

        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)

        self.btn_home = QPushButton("  Inicial")
        self.btn_home.setIcon(QIcon("assets/home.png"))
        self.btn_home.setStyleSheet(self.top_button_style())

        self.btn_profile = QPushButton("  Meu perfil")
        self.btn_profile.setIcon(QIcon("assets/user_profile.png"))
        self.btn_profile.setStyleSheet(self.top_button_style())

        top_layout.addWidget(self.btn_home)
        top_layout.addStretch()
        top_layout.addWidget(self.btn_profile)

        main_layout.addWidget(self.top_bar)

        # =============================
        # BODY (SIDEBAR + CONTENT)
        # =============================
        body = QFrame()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # ---------- SIDEBAR ----------
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(300)
        self.sidebar.setStyleSheet("background-color: #B6A8C9;")

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(10)

        # CATEGORIA
        sidebar_layout.addWidget(self.section_title("CATEGORIA"))

        sidebar_layout.addWidget(
            self.sidebar_item("assets/clear.png", "Limpeza, Higiene e Alimentos")
        )
        sidebar_layout.addWidget(
            self.sidebar_item("assets/electrical.png", "Elétrica")
        )
        sidebar_layout.addWidget(
            self.sidebar_item("assets/hydraulic_water.png", "Hidráulica")
        )
        sidebar_layout.addWidget(
            self.sidebar_item("assets/settings_tools.png", "Ferramentas Gerais")
        )
        sidebar_layout.addWidget(
            self.sidebar_item("assets/truck.png", "Automóveis")
        )
        sidebar_layout.addWidget(
            self.sidebar_item("assets/gas.png", "Abastecimento Véiculos Obras")
        )

        sidebar_layout.addWidget(self.hr_line())

        # AÇÕES
        sidebar_layout.addWidget(self.section_title("AÇÕES"))

        self.btn_sidebar_consultar = self.sidebar_item("assets/magnifier.png", "Consultar")
        self.btn_sidebar_solicitar = self.sidebar_item("assets/request.png", "Solicitar")
        self.btn_sidebar_relatorio = self.sidebar_item("assets/graphic.png", "Relatório")
        self.btn_sidebar_imprimir = self.sidebar_item("assets/print.png", "Imprimir")
        self.btn_sidebar_exportar = self.sidebar_item("assets/export.png", "Exportar")

        sidebar_layout.addWidget(self.btn_sidebar_consultar)
        sidebar_layout.addWidget(self.btn_sidebar_solicitar)
        sidebar_layout.addWidget(self.btn_sidebar_relatorio)
        sidebar_layout.addWidget(self.btn_sidebar_imprimir)
        sidebar_layout.addWidget(self.btn_sidebar_exportar)

        sidebar_layout.addWidget(self.hr_line())

        # OUTROS
        sidebar_layout.addWidget(self.section_title("OUTROS"))

        self.btn_sidebar_staff = self.sidebar_item("assets/database_icon.png", "Cadastro dos Funcionários")
        self.btn_sidebar_help = self.sidebar_item("assets/help_software.png", "Ajuda")

        sidebar_layout.addWidget(self.btn_sidebar_staff)
        sidebar_layout.addWidget(self.btn_sidebar_help)

        sidebar_layout.addStretch()

        # ---------- CONTENT AREA ----------
        self.content = QFrame()
        self.content.setStyleSheet("background-color: #EDE7F2;")

        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(20)

        # QStackedWidget com as páginas
        self.pages_stack = QStackedWidget()
        content_layout.addWidget(self.pages_stack)

        # Cria páginas
        self.page_materials = self._create_page_materials()
        self.page_consultar = self._create_page_consultar()
        self.page_solicitar = self._create_page_solicitar()
        self.page_staff = self._create_page_staff()

        self.pages_stack.addWidget(self.page_materials)  # index 0
        self.pages_stack.addWidget(self.page_consultar)  # index 1
        self.pages_stack.addWidget(self.page_solicitar)  # index 2
        self.pages_stack.addWidget(self.page_staff)      # index 3

        # Página padrão (materiais)
        self.pages_stack.setCurrentWidget(self.page_materials)

        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.content)

        main_layout.addWidget(body)

    # ==================================================================
    # PÁGINA 0 – FILTRO / MATERIAIS (categorias)
    # ==================================================================
    def _create_page_materials(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        # CARD DE FILTRO
        self.filter_card = QFrame()
        self.filter_card.setStyleSheet("""
            QFrame {
                background-color: #DDD4E6;
                border-radius: 10px;
            }
        """)

        filter_layout = QVBoxLayout(self.filter_card)
        filter_layout.setContentsMargins(20, 20, 20, 20)
        filter_layout.setSpacing(15)

        title = QLabel("FILTRO - Materiais")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #3E0F63;
        """)
        filter_layout.addWidget(title)

        fields = QGridLayout()
        fields.setHorizontalSpacing(20)
        fields.setVerticalSpacing(10)

        self.input_description = QLineEdit()
        self.input_description.setPlaceholderText("Descrição")

        self.input_item_number = QLineEdit()
        self.input_item_number.setPlaceholderText("Número Item")

        self.combo_category = QComboBox()
        self.combo_category.addItem("Selecione")

        self.combo_product = QComboBox()
        self.combo_product.addItem("Selecione")

        fields.addWidget(QLabel("Descrição"), 0, 0)
        fields.addWidget(self.input_description, 1, 0)

        fields.addWidget(QLabel("Número Item"), 0, 1)
        fields.addWidget(self.input_item_number, 1, 1)

        fields.addWidget(QLabel("Categoria"), 0, 2)
        fields.addWidget(self.combo_category, 1, 2)

        fields.addWidget(QLabel("Produto"), 2, 0)
        fields.addWidget(self.combo_product, 3, 0)

        self.btn_filter = QPushButton("FILTRAR")
        self.btn_filter.setFixedHeight(40)
        self.btn_filter.setStyleSheet("""
            QPushButton {
                background-color: #3E0F63;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px 30px;
            }
            QPushButton:hover {
                background-color: #53207E;
            }
        """)
        fields.addWidget(self.btn_filter, 3, 2, alignment=Qt.AlignRight)

        filter_layout.addLayout(fields)
        layout.addWidget(self.filter_card)

        # TABELA
        self.table_materials = QTableWidget()
        self.table_materials.setColumnCount(6)
        self.table_materials.setHorizontalHeaderLabels([
            "Nm item",
            "Descrição",
            "Produto",
            "Categoria",
            "Quantidade",
            "Un. medida"
        ])

        self.table_materials.horizontalHeader().setStretchLastSection(True)
        self.table_materials.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_materials.setAlternatingRowColors(True)

        self.table_materials.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #3E0F63;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)

        layout.addWidget(self.table_materials)
        return page

    # ==================================================================
    # PÁGINA 1 – CONSULTAR AÇÕES
    # ==================================================================
    def _create_page_consultar(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #DDD4E6;
                border-radius: 10px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        title = QLabel("FILTRO - Consultar")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #3E0F63;
        """)
        card_layout.addWidget(title)

        fields = QGridLayout()
        fields.setHorizontalSpacing(20)
        fields.setVerticalSpacing(10)

        # Campos
        self.consult_subject = QLineEdit()
        self.consult_subject.setPlaceholderText("Assunto")

        self.consult_number = QLineEdit()
        self.consult_number.setPlaceholderText("Número Ação")

        self.consult_type = QComboBox()
        self.consult_type.addItem("Selecione")

        self.consult_product = QComboBox()
        self.consult_product.addItem("Selecione")

        self.consult_obs = QLineEdit()
        self.consult_obs.setPlaceholderText("Observação")

        self.consult_date = QLineEdit()
        self.consult_date.setPlaceholderText("Data")

        # Linha 1
        fields.addWidget(QLabel("Assunto"), 0, 0)
        fields.addWidget(self.consult_subject, 1, 0)

        fields.addWidget(QLabel("Número Ação"), 0, 1)
        fields.addWidget(self.consult_number, 1, 1)

        fields.addWidget(QLabel("Tipo"), 0, 2)
        fields.addWidget(self.consult_type, 1, 2)

        # Linha 2
        fields.addWidget(QLabel("Produto"), 2, 0)
        fields.addWidget(self.consult_product, 3, 0)

        fields.addWidget(QLabel("Observação"), 2, 1)
        fields.addWidget(self.consult_obs, 3, 1)

        fields.addWidget(QLabel("Data"), 2, 2)
        fields.addWidget(self.consult_date, 3, 2)

        # Botão FILTRAR
        self.btn_consult_filter = QPushButton("FILTRAR")
        self.btn_consult_filter.setFixedHeight(40)
        self.btn_consult_filter.setStyleSheet("""
            QPushButton {
                background-color: #3E0F63;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px 30px;
            }
            QPushButton:hover {
                background-color: #53207E;
            }
        """)
        fields.addWidget(self.btn_consult_filter, 4, 2, alignment=Qt.AlignRight)

        card_layout.addLayout(fields)
        layout.addWidget(card)

        # Tabela de ações
        self.table_actions = QTableWidget()
        self.table_actions.setColumnCount(6)
        self.table_actions.setHorizontalHeaderLabels([
            "Nm_ação",
            "Assunto",
            "Obs",
            "Categoria",
            "Permitido por",
            "Data",
        ])
        self.table_actions.horizontalHeader().setStretchLastSection(True)
        self.table_actions.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_actions.setAlternatingRowColors(True)
        self.table_actions.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #3E0F63;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)

        layout.addWidget(self.table_actions)
        return page

    # ==================================================================
    # PÁGINA 2 – SOLICITAR MATERIAIS
    # ==================================================================
    def _create_page_solicitar(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #DDD4E6;
                border-radius: 10px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        title = QLabel("TABELA - Solicitar")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #3E0F63;
        """)
        card_layout.addWidget(title)

        fields = QGridLayout()
        fields.setHorizontalSpacing(20)
        fields.setVerticalSpacing(10)

        self.req_category = QComboBox()
        self.req_category.addItem("Selecione")

        self.req_type = QComboBox()
        self.req_type.addItem("Selecione")

        self.req_description = QLineEdit()
        self.req_description.setPlaceholderText("Descrição")

        fields.addWidget(QLabel("Categoria"), 0, 0)
        fields.addWidget(self.req_category, 1, 0)

        fields.addWidget(QLabel("Tipo Solicitação"), 0, 2)
        fields.addWidget(self.req_type, 1, 2)

        fields.addWidget(QLabel("Descrição"), 2, 0, 1, 3)
        fields.addWidget(self.req_description, 3, 0, 1, 3)

        card_layout.addLayout(fields)

        # Tabela de itens
        label_itens = QLabel("Itens")
        label_itens.setStyleSheet("font-weight: bold; color: #3E0F63;")
        card_layout.addWidget(label_itens)

        self.table_request_items = QTableWidget()
        self.table_request_items.setColumnCount(4)
        self.table_request_items.setHorizontalHeaderLabels([
            "Add",
            "Número Item",
            "Descrição Item",
            "Quantidade"
        ])
        self.table_request_items.horizontalHeader().setStretchLastSection(True)
        self.table_request_items.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_request_items.setAlternatingRowColors(True)
        self.table_request_items.setStyleSheet("""
            QTableWidget {
                background-color: white;
            }
            QHeaderView::section {
                background-color: #3E0F63;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)
        card_layout.addWidget(self.table_request_items)

        # Rodapé do formulário
        footer_layout = QGridLayout()
        footer_layout.setHorizontalSpacing(20)
        footer_layout.setVerticalSpacing(10)

        self.req_requested_by = QLineEdit()
        self.req_observation = QPlainTextEdit()
        self.req_authorized_by = QComboBox()
        self.req_authorized_by.addItem("Selecione")

        footer_layout.addWidget(QLabel("Solicitado por"), 0, 0)
        footer_layout.addWidget(self.req_requested_by, 1, 0)

        footer_layout.addWidget(QLabel("Observações adicionais (opcional)"), 0, 1)
        footer_layout.addWidget(self.req_observation, 1, 1, 3, 1)

        footer_layout.addWidget(QLabel("Autorizado por"), 2, 0)
        footer_layout.addWidget(self.req_authorized_by, 3, 0)

        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.btn_req_cancel = QPushButton("CANCELAR")
        self.btn_req_clear = QPushButton("LIMPAR")
        self.btn_req_confirm = QPushButton("CONFIRMAR")

        self.btn_req_cancel.setFixedWidth(140)
        self.btn_req_clear.setFixedWidth(140)
        self.btn_req_confirm.setFixedWidth(160)

        self.btn_req_cancel.setStyleSheet("""
            QPushButton {
                background-color: #C0BEC4;
                color: #3E0F63;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #B1AFB5;
            }
        """)
        self.btn_req_clear.setStyleSheet("""
            QPushButton {
                background-color: #E4D7F3;
                color: #3E0F63;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #D3C4E4;
            }
        """)
        self.btn_req_confirm.setStyleSheet("""
            QPushButton {
                background-color: #3E0F63;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px 24px;
            }
            QPushButton:hover {
                background-color: #53207E;
            }
        """)

        buttons_layout.addWidget(self.btn_req_cancel)
        buttons_layout.addWidget(self.btn_req_clear)
        buttons_layout.addWidget(self.btn_req_confirm)

        footer_layout.addLayout(buttons_layout, 4, 0, 1, 2)

        card_layout.addLayout(footer_layout)
        layout.addWidget(card)

        return page

    # ==================================================================
    # PÁGINA 3 – CADASTRO DOS FUNCIONÁRIOS
    # ==================================================================
    def _create_page_staff(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #DDD4E6;
                border-radius: 10px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(20)

        title = QLabel("TABELA – Cadastro dos Funcionários")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #3E0F63;
        """)
        card_layout.addWidget(title)

        fields = QGridLayout()
        fields.setHorizontalSpacing(30)
        fields.setVerticalSpacing(15)

        self.user_username = QLineEdit()
        self.user_fullname = QLineEdit()
        self.user_level = QComboBox()
        self.user_level.addItems(["Selecione", "BAIXO", "MÉDIO", "ALTO"])
        self.user_role = QComboBox()
        self.user_role.addItems(["Selecione", "ADMIN", "USER"])
        self.user_session = QLineEdit()
        self.user_password = QLineEdit()
        self.user_password.setEchoMode(QLineEdit.Password)
        self.user_password_confirm = QLineEdit()
        self.user_password_confirm.setEchoMode(QLineEdit.Password)

        # Linha 1
        fields.addWidget(QLabel("Nome Usuário"), 0, 0)
        fields.addWidget(self.user_username, 1, 0)

        fields.addWidget(QLabel("Nome Completo"), 0, 1, 1, 2)
        fields.addWidget(self.user_fullname, 1, 1, 1, 2)

        # Linha 2
        fields.addWidget(QLabel("Nível"), 2, 0)
        fields.addWidget(self.user_level, 3, 0)

        fields.addWidget(QLabel("Cargo"), 2, 1)
        fields.addWidget(self.user_role, 3, 1)

        fields.addWidget(QLabel("Sessão"), 2, 2)
        fields.addWidget(self.user_session, 3, 2)

        # Linha 3
        fields.addWidget(QLabel("Senha"), 4, 0, 1, 2)
        fields.addWidget(self.user_password, 5, 0, 1, 2)

        fields.addWidget(QLabel("Confirma Senha"), 4, 2)
        fields.addWidget(self.user_password_confirm, 5, 2)

        card_layout.addLayout(fields)

        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.btn_user_cancel = QPushButton("CANCELAR")
        self.btn_user_clear = QPushButton("LIMPAR")
        self.btn_user_save = QPushButton("CADASTRAR")

        for btn in (self.btn_user_cancel, self.btn_user_clear, self.btn_user_save):
            btn.setFixedWidth(150)
            btn.setFixedHeight(42)

        self.btn_user_cancel.setStyleSheet("""
            QPushButton {
                background-color: #C0BEC4;
                color: #3E0F63;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #B1AFB5;
            }
        """)
        self.btn_user_clear.setStyleSheet("""
            QPushButton {
                background-color: #E4D7F3;
                color: #3E0F63;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #D3C4E4;
            }
        """)
        self.btn_user_save.setStyleSheet("""
            QPushButton {
                background-color: #3E0F63;
                color: white;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #53207E;
            }
        """)

        buttons_layout.addWidget(self.btn_user_cancel)
        buttons_layout.addWidget(self.btn_user_clear)
        buttons_layout.addWidget(self.btn_user_save)

        card_layout.addLayout(buttons_layout)

        layout.addWidget(card)
        return page

    # ==================================================================
    # STYLES & COMPONENTS
    # ==================================================================
    def top_button_style(self):
        return """
            QPushButton {
                color: white;
                font-size: 16px;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                color: #E0C8FF;
            }
        """

    def section_title(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            font-size: 17px;
            font-weight: bold;
            color: #3A1A5E;
        """)
        return label

    def hr_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #3A1A5E; border: none;")
        return line

    def sidebar_item(self, icon_path, text):
        btn = QPushButton(text)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(24, 24))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 6px 10px;
                color: #4A2A6A;
                font-size: 15px;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #D9CFE6;
                border-radius: 6px;
            }
        """)
        return btn
