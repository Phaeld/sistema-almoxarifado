"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    Screen to control fuel supply for work vehicles.
====================================================================
"""

from qt_core import *

from gui.window.main_window.ui_control_gas_window import UI_ControlGasWindow
from auth.session import Session


class ControlGasWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Sessão
        if not Session.is_authenticated():
            self.close()
            return

        self.user = Session.get()

        # UI
        self.ui = UI_ControlGasWindow()
        self.ui.setup_ui(self)

        # Conexões
        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)

        self.ui.btn_filter.clicked.connect(self.apply_filters)
        self.ui.btn_print.clicked.connect(self.print_report)
        self.ui.btn_export.clicked.connect(self.export_report)

        self.show()

    def apply_filters(self):
        # Placeholder: implementar filtro real quando o banco estiver pronto
        pass

    def print_report(self):
        # Placeholder: implementar impressão
        pass

    def export_report(self):
        # Placeholder: implementar exportação
        pass

    def go_home(self):
        from home import HomeWindow
        self.home = HomeWindow()
        self.home.show()
        self.close()

    def open_profile(self):
        from profile import ProfileWindow
        self.profile = ProfileWindow()
        self.profile.show()
        self.close()
