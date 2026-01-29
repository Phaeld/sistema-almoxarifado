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

        self.btn_cat_limpeza = self.sidebar_item("assets/clear.png", "Limpeza, Higiene e Alimentos")
        self.btn_cat_eletrica = self.sidebar_item("assets/electrical.png", "Elétrica")
        self.btn_cat_hidraulica = self.sidebar_item("assets/hydraulic_water.png", "Hidráulica")
        self.btn_cat_ferramentas = self.sidebar_item("assets/settings_tools.png", "Ferramentas Gerais")
        self.btn_cat_automoveis = self.sidebar_item("assets/truck.png", "Automóveis")
        self.btn_cat_abastecimento = self.sidebar_item("assets/gas.png", "Abastecimento Véiculos Obras")

        sidebar_layout.addWidget(self.btn_cat_limpeza)
        sidebar_layout.addWidget(self.btn_cat_eletrica)
        sidebar_layout.addWidget(self.btn_cat_hidraulica)
        sidebar_layout.addWidget(self.btn_cat_ferramentas)
        sidebar_layout.addWidget(self.btn_cat_automoveis)
        sidebar_layout.addWidget(self.btn_cat_abastecimento)

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

        self.btn_sidebar_colaboradores = self.sidebar_item(
            "assets/database_icon.png",
            "Cadastro dos Funcionários"
        )
        self.btn_sidebar_ajuda = self.sidebar_item(
            "assets/help_software.png",
            "Ajuda"
        )

        sidebar_layout.addWidget(self.btn_sidebar_colaboradores)
        sidebar_layout.addWidget(self.btn_sidebar_ajuda)

        sidebar_layout.addStretch()

        # ---------- CONTENT AREA ----------
        self.content = QFrame()
        self.content.setStyleSheet("background-color: #EDE7F2;")

        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)

        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.content)

        main_layout.addWidget(body)

        # =============================
        # FILTER CARD (MATERIAIS)
        # =============================
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

        # Title
        title = QLabel("FILTRO - Materiais")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #3E0F63;
        """)
        filter_layout.addWidget(title)

        # Fields
        fields_layout = QGridLayout()
        fields_layout.setHorizontalSpacing(20)
        fields_layout.setVerticalSpacing(10)

        label_style = """
            font-size: 14px;
            font-weight: bold;
            color: #3A1A5E;
        """

        # Descrição
        lbl_desc = QLabel("Descrição")
        lbl_desc.setStyleSheet(label_style)
        self.input_description = QLineEdit()
        self.input_description.setPlaceholderText("Descrição")
        self.input_description.setStyleSheet(self.input_style())

        # Número item
        lbl_num = QLabel("Número Item")
        lbl_num.setStyleSheet(label_style)
        self.input_item_number = QLineEdit()
        self.input_item_number.setPlaceholderText("Número Item")
        self.input_item_number.setStyleSheet(self.input_style())

        # Categoria
        lbl_cat = QLabel("Categoria")
        lbl_cat.setStyleSheet(label_style)
        self.combo_category = QComboBox()
        self.combo_category.setStyleSheet(self.combo_style())
        self.combo_category.addItem("Selecione")
        self.combo_category.addItems([
            "ELETRICA",
            "HIDRAULICA",
            "LIMPEZA_HIGIENE_ALIMENTOS",
            "FERRAMENTAS_GERAIS",
            "AUTOMOVEIS",
        ])

        # Produto
        lbl_prod = QLabel("Produto")
        lbl_prod.setStyleSheet(label_style)
        self.combo_product = QComboBox()
        self.combo_product.setStyleSheet(self.combo_style())
        self.combo_product.addItem("Selecione")
        # self.combo_product.addItems([
        #     "Disjuntor",
        #     "Relé",
        #     "Tomada",
        #     "Lâmpada",
        #     "EPI",
        # ])

        fields_layout.addWidget(lbl_desc, 0, 0)
        fields_layout.addWidget(self.input_description, 1, 0)

        fields_layout.addWidget(lbl_num, 0, 1)
        fields_layout.addWidget(self.input_item_number, 1, 1)

        fields_layout.addWidget(lbl_cat, 0, 2)
        fields_layout.addWidget(self.combo_category, 1, 2)

        fields_layout.addWidget(lbl_prod, 2, 0)
        fields_layout.addWidget(self.combo_product, 3, 0)

        # Filter button
        self.btn_filter = QPushButton("FILTRAR")
        self.btn_filter.setFixedHeight(40)
        self.btn_filter.setCursor(Qt.PointingHandCursor)
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

        fields_layout.addWidget(self.btn_filter, 3, 2, alignment=Qt.AlignRight)

        filter_layout.addLayout(fields_layout)
        self.content_layout.addWidget(self.filter_card)

        # =============================
        # TABLE (MATERIAIS)
        # =============================
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

        header = self.table_materials.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.table_materials.setAlternatingRowColors(True)

        self.table_materials.setStyleSheet("""
            QTableWidget {
                background-color: #F6EFFB;
                alternate-background-color: #E4D4F3;
                color: #3E0F63;
                border-radius: 6px;
            }
            QTableWidget::item {
                color: #3E0F63;
            }
            QHeaderView::section {
                background-color: #3E0F63;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)

        self.content_layout.addWidget(self.table_materials)

    # =============================
    # STYLES & COMPONENTS
    # =============================
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

    def input_style(self):
        return """
            QLineEdit {
                background-color: #E8E2EE;
                border-radius: 6px;
                padding: 6px 8px;
                border: 1px solid #C1B2D9;
                color: #3E0F63;
            }
        """

    def combo_style(self):
        return """
            QComboBox {
                background-color: #E8E2EE;
                border-radius: 6px;
                padding: 4px 8px;
                border: 1px solid #C1B2D9;
                color: #3E0F63;
            }
            QComboBox::drop-down {
                border: none;
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
