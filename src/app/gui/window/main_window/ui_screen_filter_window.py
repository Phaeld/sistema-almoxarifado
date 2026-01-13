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


# SCREEN FILTER WINDOW
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

        # TOP BAR
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

        # BODY (SIDEBAR + CONTENT)
        body = QFrame()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # SIDEBAR
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(300)
        self.sidebar.setStyleSheet("background-color: #B6A8C9;")

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(10)

        # CATEGORY
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

        # ACTIONS
        sidebar_layout.addWidget(self.section_title("AÇÕES"))

        sidebar_layout.addWidget(
            self.sidebar_item("assets/magnifier.png", "Consultar")
        )
        sidebar_layout.addWidget(
            self.sidebar_item("assets/request.png", "Solicitar")
        )
        sidebar_layout.addWidget(
            self.sidebar_item("assets/graphic.png", "Relatório")
        )
        sidebar_layout.addWidget(
            self.sidebar_item("assets/print.png", "Imprimir")
        )
        sidebar_layout.addWidget(
            self.sidebar_item("assets/export.png", "Exportar")
        )

        sidebar_layout.addWidget(self.hr_line())

        # OTHERS
        sidebar_layout.addWidget(self.section_title("OUTROS"))

        sidebar_layout.addWidget(
            self.sidebar_item("assets/database_icon.png", "Cadastro dos Funcionários")
        )
        sidebar_layout.addWidget(
            self.sidebar_item("assets/help_software.png", "Ajuda")
        )

        sidebar_layout.addStretch()

        # CONTENT AREA
        self.content = QFrame()
        self.content.setStyleSheet("background-color: #EDE7F2;")

        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.content)

        main_layout.addWidget(body)

    # STYLES & COMPONENTS
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

    # COMPONENTS
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