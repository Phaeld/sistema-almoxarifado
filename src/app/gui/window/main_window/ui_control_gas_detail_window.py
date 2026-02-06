"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    Simple detail screen for a fuel control record.
====================================================================
"""

from qt_core import *
from gui import resources_rc


class UI_ControlGasDetailWindow(object):
    def setup_ui(self, parent: QMainWindow):
        if not parent.objectName():
            parent.setObjectName("ControlGasDetailWindow")

        parent.resize(900, 560)
        parent.setMinimumSize(800, 480)
        parent.setWindowTitle("Almoxarifado Obras - Detalhes Abastecimento")
        parent.setWindowIcon(QIcon("assets/icon.jpg"))
        parent.setStyleSheet("background-color: #E8E2EE;")

        self.central_widget = QWidget(parent)
        parent.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(16)

        title = QLabel("DETALHES DO ABASTECIMENTO")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #3E0F63;
            }
        """)
        main_layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #D9CEE6;
                border-radius: 12px;
            }
        """)
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(24)

        # LEFT DETAILS
        left = QFrame()
        left_layout = QGridLayout(left)
        left_layout.setHorizontalSpacing(30)
        left_layout.setVerticalSpacing(16)

        label_style = "font-size: 13px; font-weight: bold; color: #3A1A5E;"
        value_style = "font-size: 13px; color: #3A1A5E;"

        def make_row(text):
            lbl = QLabel(text)
            lbl.setStyleSheet(label_style)
            val = QLabel("")
            val.setStyleSheet(value_style)
            return lbl, val

        self.lbl_id, self.val_id = make_row("ID:")
        self.lbl_vehicle, self.val_vehicle = make_row("VEICULO:")
        self.lbl_plate, self.val_plate = make_row("PLACA:")
        self.lbl_date, self.val_date = make_row("DATA:")
        self.lbl_driver, self.val_driver = make_row("MOTORISTA:")
        self.lbl_odo_type, self.val_odo_type = make_row("TIPO ODOMETRO:")
        self.lbl_odo, self.val_odo = make_row("NUMERO ODOMETRO:")
        self.lbl_diff, self.val_diff = make_row("DIFERENCA:")
        self.lbl_liters, self.val_liters = make_row("LITROS ABASTECIDOS:")
        self.lbl_avg, self.val_avg = make_row("MEDIA:")
        self.lbl_fuel, self.val_fuel = make_row("TIPO COMBUSTIVEL:")
        self.lbl_value, self.val_value = make_row("VALOR R$:")

        left_layout.addWidget(self.lbl_id, 0, 0)
        left_layout.addWidget(self.val_id, 0, 1)
        left_layout.addWidget(self.lbl_vehicle, 0, 2)
        left_layout.addWidget(self.val_vehicle, 0, 3)
        left_layout.addWidget(self.lbl_plate, 0, 4)
        left_layout.addWidget(self.val_plate, 0, 5)

        left_layout.addWidget(self.lbl_date, 1, 0)
        left_layout.addWidget(self.val_date, 1, 1)
        left_layout.addWidget(self.lbl_driver, 1, 2)
        left_layout.addWidget(self.val_driver, 1, 3)
        left_layout.addWidget(self.lbl_odo_type, 1, 4)
        left_layout.addWidget(self.val_odo_type, 1, 5)

        left_layout.addWidget(self.lbl_odo, 2, 0)
        left_layout.addWidget(self.val_odo, 2, 1)
        left_layout.addWidget(self.lbl_diff, 2, 2)
        left_layout.addWidget(self.val_diff, 2, 3)

        left_layout.addWidget(self.lbl_liters, 3, 0)
        left_layout.addWidget(self.val_liters, 3, 1)
        left_layout.addWidget(self.lbl_avg, 3, 2)
        left_layout.addWidget(self.val_avg, 3, 3)

        left_layout.addWidget(self.lbl_fuel, 4, 0)
        left_layout.addWidget(self.val_fuel, 4, 1)
        left_layout.addWidget(self.lbl_value, 4, 2)
        left_layout.addWidget(self.val_value, 4, 3)

        # Close button
        self.btn_close = QPushButton("FECHAR")
        self.btn_close.setFixedWidth(120)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #3E0F63;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #53207E;
            }
        """)
        left_layout.addWidget(self.btn_close, 5, 2, alignment=Qt.AlignLeft)

        # RIGHT PHOTO
        right = QFrame()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setAlignment(Qt.AlignCenter)

        self.photo = QLabel("FOTO")
        self.photo.setAlignment(Qt.AlignCenter)
        self.photo.setFixedSize(200, 200)
        self.photo.setStyleSheet("""
            QLabel {
                background-color: #A35CB5;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
            }
        """)
        right_layout.addWidget(self.photo)

        card_layout.addWidget(left, stretch=3)
        card_layout.addWidget(right, stretch=1)

        main_layout.addWidget(card)
