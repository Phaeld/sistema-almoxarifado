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
from gui.window.main_window.ui_main_window import UI_MainWindow
from home import HomeWindow

# MAIN WINDOW
class MainWindow(QMainWindow):    
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOW
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # PAGE INTERACTIONS
        self.ui.login_button.clicked.connect(self.go_to_home)
        self.ui.user_input.returnPressed.connect(self.go_to_home)
        self.ui.pass_input.returnPressed.connect(self.go_to_home)

    # FUNCTION TO GO TO HOME PAGE
    def go_to_home(self):
        self.home = HomeWindow()
        self.home.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())