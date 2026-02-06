"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    Report window with charts for fuel control.
====================================================================
"""

from qt_core import *
from gui import resources_rc


class UI_ControlGasReportWindow(object):
    def setup_ui(self, parent: QMainWindow):
        if not parent.objectName():
            parent.setObjectName("ControlGasReportWindow")

        parent.resize(1200, 720)
        parent.setMinimumSize(960, 540)
        parent.setWindowTitle("Almoxarifado Obras - Relatorio Abastecimento")
        parent.setWindowIcon(QIcon("assets/icon.jpg"))
        parent.setStyleSheet("background-color: #E8E2EE;")

        self.central_widget = QWidget(parent)
        parent.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        title = QLabel("RELATORIO DE ABASTECIMENTO")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #3E0F63;
            }
        """)
        main_layout.addWidget(title)

        # Controls row
        controls = QFrame()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)

        self.period_group = QButtonGroup(parent)
        self.radio_daily = QRadioButton("Diario")
        self.radio_weekly = QRadioButton("Semanal")
        self.radio_monthly = QRadioButton("Mensal")
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

        for i, r in enumerate([self.radio_daily, self.radio_weekly, self.radio_monthly]):
            r.setStyleSheet(radio_style)
            self.period_group.addButton(r, i)
            controls_layout.addWidget(r)

        # Month filter
        self.combo_month = QComboBox()
        self.combo_month.addItem("Todos os meses")
        self.combo_month.addItems([
            "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ])
        self.combo_month.setStyleSheet("""
            QComboBox {
                background-color: #E8E2EE;
                border-radius: 8px;
                padding: 4px 10px;
                border: 1px solid #CBB2E6;
                color: #3A1A5E;
            }
        """)
        controls_layout.addSpacing(12)
        controls_layout.addWidget(self.combo_month)

        controls_layout.addStretch()
        self.btn_generate = QPushButton("GERAR")
        self.btn_generate.setStyleSheet(self._primary_button())
        controls_layout.addWidget(self.btn_generate)
        main_layout.addWidget(controls)

        # Summary row
        summary = QHBoxLayout()
        self.lbl_total = QLabel("Total gasto: R$")
        self.lbl_total.setStyleSheet("font-size: 14px; font-weight: bold; color: #3A1A5E;")
        self.lbl_top_vehicle = QLabel("Veiculo que mais abasteceu: -")
        self.lbl_top_vehicle.setStyleSheet("font-size: 14px; font-weight: bold; color: #3A1A5E;")
        summary.addWidget(self.lbl_total)
        summary.addStretch()
        summary.addWidget(self.lbl_top_vehicle)
        main_layout.addLayout(summary)

        # Content grid
        content = QHBoxLayout()

        self.chart_label = QLabel()
        self.chart_label.setMinimumSize(700, 360)
        self.chart_label.setStyleSheet("""
            QLabel {
                background-color: #D9CEE6;
                border-radius: 12px;
            }
        """)
        self.chart_label.setAlignment(Qt.AlignCenter)

        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background-color: #D9CEE6;
                border-radius: 12px;
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(8)

        right_title = QLabel("Resumo por placa")
        right_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #3A1A5E;")
        right_layout.addWidget(right_title)

        self.table_summary = QTableWidget()
        self.table_summary.setColumnCount(3)
        self.table_summary.setHorizontalHeaderLabels(["Placa", "Media Consumo", "Media Valor"])
        self.table_summary.horizontalHeader().setStretchLastSection(True)
        self.table_summary.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_summary.verticalHeader().setVisible(False)
        self.table_summary.setAlternatingRowColors(True)
        self.table_summary.setStyleSheet("""
            QTableWidget {
                background-color: #F6F1FA;
                gridline-color: #CBB2E6;
                color: #3A1A5E;
            }
            QHeaderView::section {
                background-color: #9B3D97;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border: none;
                padding: 6px;
            }
        """)
        right_layout.addWidget(self.table_summary)

        content.addWidget(self.chart_label, stretch=3)
        content.addWidget(right_panel, stretch=1)

        main_layout.addLayout(content)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_print = QPushButton("IMPRIMIR")
        self.btn_print.setStyleSheet(self._primary_button())

        self.btn_close = QPushButton("FECHAR")
        self.btn_close.setStyleSheet(self._secondary_button())

        btn_row.addWidget(self.btn_print)
        btn_row.addWidget(self.btn_close)
        btn_row.addStretch()
        main_layout.addLayout(btn_row)

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
