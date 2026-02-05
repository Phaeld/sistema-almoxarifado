"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    Fuel control form screen (Cadastro de Abastecimento).
====================================================================
"""

from qt_core import *
from gui import resources_rc


class UI_ControlGasFormWindow(object):
    def setup_ui(self, parent: QMainWindow):
        if not parent.objectName():
            parent.setObjectName("ControlGasFormWindow")

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
        #  FORM CARD
        # =============================
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #D9CEE6;
                border-radius: 12px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 25, 35, 30)
        card_layout.setSpacing(16)

        title = QLabel("TABELA - Controle de Abastecimento")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #3E0F63;
            }
        """)
        card_layout.addWidget(title)

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

        grid = QGridLayout()
        grid.setHorizontalSpacing(26)
        grid.setVerticalSpacing(18)

        # Carro
        lbl_car = QLabel("Carro")
        lbl_car.setStyleSheet(label_style)
        self.combo_car = QComboBox()
        self.combo_car.setStyleSheet(combo_style)
        self.combo_car.addItem("Selecione")

        # Motorista
        lbl_driver = QLabel("Motorista")
        lbl_driver.setStyleSheet(label_style)
        self.input_driver = QLineEdit()
        self.input_driver.setStyleSheet(line_style)

        # Número placa
        lbl_plate = QLabel("Número placa")
        lbl_plate.setStyleSheet(label_style)
        self.combo_plate = QComboBox()
        self.combo_plate.setStyleSheet(combo_style)
        self.combo_plate.addItem("Selecione")

        # Tipo odometro
        lbl_odo_type = QLabel("Tipo de odometro")
        lbl_odo_type.setStyleSheet(label_style)
        self.combo_odo_type = QComboBox()
        self.combo_odo_type.setStyleSheet(combo_style)
        self.combo_odo_type.addItem("Selecione")

        # Tipo combustível
        lbl_fuel = QLabel("Tipo Combustível")
        lbl_fuel.setStyleSheet(label_style)
        self.combo_fuel = QComboBox()
        self.combo_fuel.setStyleSheet(combo_style)
        self.combo_fuel.addItem("Selecione")

        # Número do odômetro
        lbl_odo = QLabel("Número do Odômetro")
        lbl_odo.setStyleSheet(label_style)
        self.input_odo = QLineEdit()
        self.input_odo.setStyleSheet(line_style)

        # Quantidade litros
        lbl_qty = QLabel("Quantidade de Litros Abastecido")
        lbl_qty.setStyleSheet(label_style)
        self.input_qty = QLineEdit()
        self.input_qty.setStyleSheet(line_style)

        # Valor
        lbl_value = QLabel("Valor")
        lbl_value.setStyleSheet(label_style)
        self.input_value = QLineEdit()
        self.input_value.setStyleSheet(line_style)

        grid.addWidget(lbl_car, 0, 0)
        grid.addWidget(self.combo_car, 1, 0)
        grid.addWidget(lbl_driver, 0, 1)
        grid.addWidget(self.input_driver, 1, 1, 1, 2)

        grid.addWidget(lbl_plate, 2, 0)
        grid.addWidget(self.combo_plate, 3, 0)
        grid.addWidget(lbl_odo_type, 2, 1)
        grid.addWidget(self.combo_odo_type, 3, 1)
        grid.addWidget(lbl_fuel, 2, 2)
        grid.addWidget(self.combo_fuel, 3, 2)

        grid.addWidget(lbl_odo, 4, 0)
        grid.addWidget(self.input_odo, 5, 0)
        grid.addWidget(lbl_qty, 4, 1)
        grid.addWidget(self.input_qty, 5, 1, 1, 2)

        grid.addWidget(lbl_value, 6, 0)
        grid.addWidget(self.input_value, 7, 0, 1, 2)

        card_layout.addLayout(grid)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_cancel = QPushButton("CANCELAR")
        self.btn_cancel.setStyleSheet(self._secondary_button())

        self.btn_clear = QPushButton("LIMPAR")
        self.btn_clear.setStyleSheet(self._light_button())

        self.btn_register = QPushButton("CADASTRAR")
        self.btn_register.setStyleSheet(self._primary_button())

        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_clear)
        btn_row.addWidget(self.btn_register)
        btn_row.addStretch()

        card_layout.addSpacing(8)
        card_layout.addLayout(btn_row)

        # Center card
        wrapper = QWidget()
        wrapper_layout = QHBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(60, 25, 60, 25)
        wrapper_layout.addWidget(card)

        main_layout.addWidget(wrapper)

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
                padding: 8px 22px;
            }
            QPushButton:hover {
                background-color: #53207E;
            }
        """

    def _secondary_button(self) -> str:
        return """
            QPushButton {
                background-color: #B5B1C2;
                color: #3A1A5E;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
                padding: 8px 22px;
            }
            QPushButton:hover {
                background-color: #9E99AF;
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
                padding: 8px 22px;
            }
            QPushButton:hover {
                background-color: #DDC8F0;
            }
        """
