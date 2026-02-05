"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    Fuel control screen (Abastecimento).
====================================================================
"""

from qt_core import *
from gui import resources_rc


class UI_ControlGasWindow(object):
    def setup_ui(self, parent: QMainWindow):
        if not parent.objectName():
            parent.setObjectName("ControlGasWindow")

        parent.resize(1200, 720)
        parent.setMinimumSize(960, 540)
        parent.setWindowTitle("Almoxarifado Obras - Abastecimento")
        parent.setWindowIcon(QIcon("assets/icon.jpg"))
        parent.setStyleSheet("background-color: #E8E2EE;")

        # CENTRAL
        self.central_widget = QWidget(parent)
        parent.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =============================
        #  TOP BAR
        # =============================
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(50)
        self.top_bar.setStyleSheet("background-color: #390E68;")

        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)

        self.btn_home = QPushButton("  Inicial")
        self.btn_home.setIcon(QIcon("assets/home.png"))
        self.btn_home.setStyleSheet(self._top_button_style())

        self.btn_profile = QPushButton("  Meu perfil")
        self.btn_profile.setIcon(QIcon("assets/user_profile.png"))
        self.btn_profile.setStyleSheet(self._top_button_style())

        top_layout.addWidget(self.btn_home)
        top_layout.addStretch()
        top_layout.addWidget(self.btn_profile)

        main_layout.addWidget(self.top_bar)

        # =============================
        #  BODY
        # =============================
        body = QFrame()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(30, 25, 30, 25)
        body_layout.setSpacing(25)

        # LEFT TOOLBOX
        self.toolbox = QFrame()
        self.toolbox.setFixedWidth(300)
        self.toolbox.setStyleSheet("""
            QFrame {
                background-color: #D6CBE2;
                border-radius: 12px;
            }
        """)
        toolbox_layout = QVBoxLayout(self.toolbox)
        toolbox_layout.setContentsMargins(16, 18, 16, 16)
        toolbox_layout.setSpacing(10)

        title = QLabel("FERRAMENTAS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #3A1A5E;
            }
        """)
        toolbox_layout.addWidget(title)

        tools_grid = QGridLayout()
        tools_grid.setSpacing(10)

        self.btn_tool_add_car = self._tool_button("assets/add_car.png")
        self.btn_tool_remove_car = self._tool_button("assets/delete_car.png")
        self.btn_tool_edit_car = self._tool_button("assets/edit_car.png")
        self.btn_tool_add_file = self._tool_button("assets/add_file.png")
        self.btn_tool_remove_file = self._tool_button("assets/remove_file.png")
        self.btn_tool_write = self._tool_button("assets/writing.png")

        tools_grid.addWidget(self.btn_tool_add_car, 0, 0)
        tools_grid.addWidget(self.btn_tool_remove_car, 0, 1)
        tools_grid.addWidget(self.btn_tool_edit_car, 0, 2)
        tools_grid.addWidget(self.btn_tool_add_file, 1, 0)
        tools_grid.addWidget(self.btn_tool_remove_file, 1, 1)
        tools_grid.addWidget(self.btn_tool_write, 1, 2)

        toolbox_layout.addLayout(tools_grid)
        toolbox_layout.addStretch()

        btn_row = QHBoxLayout()
        self.btn_print = QPushButton("IMPRIMIR")
        self.btn_print.setStyleSheet(self._light_button())
        self.btn_export = QPushButton("EXPORTAR")
        self.btn_export.setStyleSheet(self._primary_button())
        btn_row.addWidget(self.btn_print)
        btn_row.addWidget(self.btn_export)
        toolbox_layout.addLayout(btn_row)

        # RIGHT CONTENT
        content = QFrame()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)

        # FILTER CARD
        filter_card = QFrame()
        filter_card.setStyleSheet("""
            QFrame {
                background-color: #D9CEE6;
                border-radius: 10px;
            }
        """)
        filter_layout = QVBoxLayout(filter_card)
        filter_layout.setContentsMargins(20, 16, 20, 16)
        filter_layout.setSpacing(10)

        filter_title = QLabel("FILTRO - Abastecimento")
        filter_title.setAlignment(Qt.AlignCenter)
        filter_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #3E0F63;
            }
        """)
        filter_layout.addWidget(filter_title)

        form_grid = QGridLayout()
        form_grid.setHorizontalSpacing(20)
        form_grid.setVerticalSpacing(12)

        label_style = """
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #3A1A5E;
            }
        """
        line_style = """
            QLineEdit {
                background-color: #B7A7C6;
                border-radius: 8px;
                padding: 6px 10px;
                border: none;
                color: #3A1A5E;
            }
        """
        combo_style = """
            QComboBox {
                background-color: #B7A7C6;
                border-radius: 8px;
                padding: 4px 10px;
                border: none;
                color: #3A1A5E;
            }
        """

        lbl_vehicle = QLabel("Veículo")
        lbl_vehicle.setStyleSheet(label_style)
        self.input_vehicle = QLineEdit()
        self.input_vehicle.setStyleSheet(line_style)

        lbl_plate = QLabel("Placa")
        lbl_plate.setStyleSheet(label_style)
        self.input_plate = QLineEdit()
        self.input_plate.setStyleSheet(line_style)

        lbl_driver = QLabel("Motorista")
        lbl_driver.setStyleSheet(label_style)
        self.input_driver = QLineEdit()
        self.input_driver.setStyleSheet(line_style)

        lbl_fuel = QLabel("Tipo Combustível")
        lbl_fuel.setStyleSheet(label_style)
        self.combo_fuel = QComboBox()
        self.combo_fuel.setStyleSheet(combo_style)
        self.combo_fuel.addItem("Selecione")

        lbl_date = QLabel("Data")
        lbl_date.setStyleSheet(label_style)
        self.input_date = QLineEdit()
        self.input_date.setStyleSheet(line_style)

        self.btn_filter = QPushButton("FILTRAR")
        self.btn_filter.setFixedHeight(36)
        self.btn_filter.setStyleSheet(self._primary_button())

        form_grid.addWidget(lbl_vehicle, 0, 0)
        form_grid.addWidget(self.input_vehicle, 1, 0)
        form_grid.addWidget(lbl_plate, 0, 1)
        form_grid.addWidget(self.input_plate, 1, 1)
        form_grid.addWidget(lbl_driver, 0, 2)
        form_grid.addWidget(self.input_driver, 1, 2)
        form_grid.addWidget(lbl_fuel, 2, 0)
        form_grid.addWidget(self.combo_fuel, 3, 0)
        form_grid.addWidget(lbl_date, 2, 1)
        form_grid.addWidget(self.input_date, 3, 1)
        form_grid.addWidget(self.btn_filter, 3, 2, alignment=Qt.AlignRight)

        filter_layout.addLayout(form_grid)
        content_layout.addWidget(filter_card)

        # TITLE
        main_title = QLabel("CONTROLE ABASTECIMENTO OBRAS")
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: bold;
                color: #A35CB5;
            }
        """)
        content_layout.addWidget(main_title)

        # TABLE
        self.table_gas = QTableWidget()
        self.table_gas.setColumnCount(10)
        self.table_gas.setHorizontalHeaderLabels([
            "Veículo", "Placa", "Data", "Motorista",
            "Km/h Máq", "Diferença Km/h Máq",
            "Qnt Combustível L", "Média Consumo",
            "Tipo Combustível", "Preço R$"
        ])
        self._style_table(self.table_gas)
        content_layout.addWidget(self.table_gas)

        body_layout.addWidget(self.toolbox)
        body_layout.addWidget(content)

        main_layout.addWidget(body)

    def _tool_button(self, icon_path: str) -> QPushButton:
        btn = QPushButton()
        btn.setFixedSize(48, 48)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(28, 28))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #5B2A86;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #E5DAF2;
            }
        """)
        return btn

    def _style_table(self, table: QTableWidget):
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #F6F1FA;
                gridline-color: #CBB2E6;
                color: #3A1A5E;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #9B3D97;
                color: white;
                font-weight: bold;
                font-size: 13px;
                border: none;
                padding: 6px;
            }
        """)

    def _top_button_style(self) -> str:
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

    def _primary_button(self) -> str:
        return """
            QPushButton {
                background-color: #3E0F63;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
                padding: 8px 24px;
            }
            QPushButton:hover {
                background-color: #53207E;
            }
        """

    def _light_button(self) -> str:
        return """
            QPushButton {
                background-color: #EADDF8;
                color: #3A1A5E;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #DDC8F0;
            }
        """
