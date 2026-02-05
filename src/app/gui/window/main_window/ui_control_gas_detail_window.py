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
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        title = QLabel("DETALHES DO ABASTECIMENTO")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
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
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(10)

        self.lbl_content = QLabel("")
        self.lbl_content.setWordWrap(True)
        self.lbl_content.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #3A1A5E;
            }
        """)
        card_layout.addWidget(self.lbl_content)

        self.btn_close = QPushButton("FECHAR")
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #3E0F63;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
                padding: 6px 18px;
            }
            QPushButton:hover {
                background-color: #53207E;
            }
        """)
        card_layout.addWidget(self.btn_close, alignment=Qt.AlignCenter)

        main_layout.addWidget(card)
