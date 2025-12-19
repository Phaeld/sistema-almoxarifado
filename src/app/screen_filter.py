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

# IMPORT MAIN WINDOW
from gui.window.main_window.ui_screen_filter_window import UI_ScreenFilterWindow

# MAIN WINDOW
class ScreenFilterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #SETUP MAIN WINDOW
        self.ui = UI_ScreenFilterWindow()
        self.ui.setup_ui(self)

        # PRINT WINDOW
        self.show()

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = ScreenFilterWindow()
   sys.exit(app.exec())