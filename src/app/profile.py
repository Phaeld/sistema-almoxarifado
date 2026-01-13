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

# IMPORT MAIN WINDOW AND HOME
from gui.window.main_window.ui_profile_window import UI_ProfileWindow

# MAIN WINDOW
class ProfileWindow(QMainWindow):    
    def __init__(self, on_logout=None):
        super().__init__()

        self.on_logout = on_logout

        # SETUP MAIN WINDOW
        self.ui = UI_ProfileWindow()
        self.ui.setup_ui(self)

        # PAGE INTERACTIONS
        self.ui.btn_home.clicked.connect(self.go_to_home)
        self.ui.btn_sair.clicked.connect(self.logout)

    # FUNCTION TO GO TO HOME PAGE
    def go_to_home(self):
        from home import HomeWindow
        self.home = HomeWindow()
        self.home.show()
        self.hide()

    # LOGOUT
    def logout(self):
        if self.on_logout:
            self.on_logout()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileWindow()
    window.show()
    sys.exit(app.exec())