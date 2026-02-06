"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    Export options screen (PDF/CSV) for fuel control.
====================================================================
"""

from qt_core import *
from gui import resources_rc


class UI_ControlGasExportWindow(object):
    def setup_ui(self, parent: QMainWindow):
        if not parent.objectName():
            parent.setObjectName("ControlGasExportWindow")

        parent.resize(720, 520)
        parent.setMinimumSize(640, 480)
        parent.setWindowTitle("Almoxarifado Obras - Exportar Relatorio")
        parent.setWindowIcon(QIcon("assets/icon.jpg"))
        parent.setStyleSheet("background-color: #E8E2EE;")

        self.central_widget = QWidget(parent)
        parent.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(16)

        title = QLabel("EXPORTAR RELATORIO")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
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
        card_layout.setContentsMargins(24, 20, 24, 20)
        card_layout.setSpacing(16)

        # Period group
        period_title = QLabel("Periodo do relatorio")
        period_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #3A1A5E;")
        card_layout.addWidget(period_title)

        self.period_group = QButtonGroup(parent)
        self.radio_monthly = QRadioButton("Mensal")
        self.radio_quarterly = QRadioButton("Trimestral")
        self.radio_semiannual = QRadioButton("Semestral")
        self.radio_annual = QRadioButton("Anual")
        self.radio_monthly.setChecked(True)

        radio_style = """
            QRadioButton {
                font-size: 13px;
                color: #3A1A5E;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid #6F4C8F;
                background: #E8E2EE;
            }
            QRadioButton::indicator:checked {
                background: #3E0F63;
                border: 2px solid #3E0F63;
            }
        """

        for i, r in enumerate([
            self.radio_monthly,
            self.radio_quarterly,
            self.radio_semiannual,
            self.radio_annual,
        ]):
            r.setStyleSheet(radio_style)
            self.period_group.addButton(r, i)

        period_row = QHBoxLayout()
        period_row.addWidget(self.radio_monthly)
        period_row.addWidget(self.radio_quarterly)
        period_row.addWidget(self.radio_semiannual)
        period_row.addWidget(self.radio_annual)
        period_row.addStretch()
        card_layout.addLayout(period_row)

        # Format group
        format_title = QLabel("Formato de exportacao")
        format_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #3A1A5E;")
        card_layout.addWidget(format_title)

        self.format_group = QButtonGroup(parent)
        self.radio_csv = QRadioButton("CSV")
        self.radio_pdf = QRadioButton("PDF")
        self.radio_csv.setChecked(True)

        for i, r in enumerate([self.radio_csv, self.radio_pdf]):
            r.setStyleSheet(radio_style)
            self.format_group.addButton(r, i)

        format_row = QHBoxLayout()
        format_row.addWidget(self.radio_csv)
        format_row.addWidget(self.radio_pdf)
        format_row.addStretch()
        card_layout.addLayout(format_row)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_cancel = QPushButton("CANCELAR")
        self.btn_cancel.setStyleSheet(self._secondary_button())

        self.btn_export = QPushButton("EXPORTAR")
        self.btn_export.setStyleSheet(self._primary_button())

        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_export)
        btn_row.addStretch()
        card_layout.addLayout(btn_row)

        main_layout.addWidget(card)

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
