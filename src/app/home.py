"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    This program was developed to manage the internal warehouse
    operations of the company, allowing control of inventory,
    product registrations, incoming and outgoing materials, and
    report generation.

    The system will be implemented in Python using a graphical
    user interface (GUI) and database integration. The goal is to
    provide a practical, intuitive, and efficient solution for the
    management of internally used materials.
====================================================================
"""

# IMPORT LIBRARIES
import sys
import os

# IMPORT QT CORE
from qt_core import *

# IMPORT HOME WINDOW
from gui.window.main_window.ui_home_window import UI_HomeWindow

# HOME WINDOW
class HomeWindow(QMainWindow):
    def __init__(self, on_logout=None):
        super().__init__()

        self.on_logout = on_logout

        # SETUP HOME WINDOW
        self.ui = UI_HomeWindow()
        self.ui.setup_ui(self)

        self.ui.btn_sair.clicked.connect(self.logout)

        self.show()

    def logout(self):
        if self.on_logout:
            self.on_logout()
        self.close()

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = HomeWindow()
   sys.exit(app.exec())