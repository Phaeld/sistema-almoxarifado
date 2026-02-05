"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    Vehicle registration screen (Cadastro de Veículos).
====================================================================
"""

from qt_core import *
from gui import resources_rc


class UI_ControlGasVehicleWindow(object):
    def setup_ui(self, parent: QMainWindow, action_mode: str = "register"):
        if not parent.objectName():
            parent.setObjectName("ControlGasVehicleWindow")

        parent.resize(1200, 720)
        parent.setMinimumSize(960, 540)
        parent.setWindowTitle("Almoxarifado Obras - Cadastro de Veículos")
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
        card_layout.setSpacing(20)

        self.title = QLabel("TABELA - Cadastro de Veículos")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #3E0F63;
            }
        """)
        card_layout.addWidget(self.title)

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

        # Número placa
        lbl_plate = QLabel("Número Placa")
        lbl_plate.setStyleSheet(label_style)
        self.input_plate = QLineEdit()
        self.input_plate.setStyleSheet(line_style)

        # Tipo de odometro
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

        grid.addWidget(lbl_car, 0, 0)
        grid.addWidget(self.combo_car, 1, 0)
        grid.addWidget(lbl_plate, 0, 1)
        grid.addWidget(self.input_plate, 1, 1, 1, 2)

        grid.addWidget(lbl_odo_type, 2, 0)
        grid.addWidget(self.combo_odo_type, 3, 0)
        grid.addWidget(lbl_fuel, 2, 2)
        grid.addWidget(self.combo_fuel, 3, 2)

        card_layout.addLayout(grid)

        # Photo button
        self.btn_photo = QPushButton("SELECIONAR FOTO DO\nVEÍCULO")
        self.btn_photo.setFixedHeight(58)
        self.btn_photo.setStyleSheet("""
            QPushButton {
                background-color: #A35CB5;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 12px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #8F4FA1;
            }
        """)
        card_layout.addWidget(self.btn_photo, alignment=Qt.AlignCenter)

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

        # Set action mode (register/edit/delete)
        self.set_action_mode(action_mode)

    def set_action_mode(self, mode: str):
        mode = (mode or "register").lower()
        if mode == "delete":
            self.title.setText("TABELA - Excluir Veículos")
            self.btn_register.setText("DELETAR")
        elif mode == "edit":
            self.title.setText("TABELA - Editar Veículos")
            self.btn_register.setText("EDITAR")
        else:
            self.title.setText("TABELA - Cadastro de Veículos")
            self.btn_register.setText("CADASTRAR")

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
