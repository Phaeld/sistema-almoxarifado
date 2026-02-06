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

# IMPORT AUTH
from auth.auth_service import AuthService
from auth.session import Session



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        self.ui.login_button.clicked.connect(self.try_login)
        self.ui.pass_input.returnPressed.connect(self.try_login)
        self.ui.user_input.textChanged.connect(self.clear_error)
        self.ui.pass_input.textChanged.connect(self.clear_error)

    def try_login(self):
        username = self.ui.user_input.text()
        password = self.ui.pass_input.text()

        user = AuthService.authenticate(username, password)

        if user:
            Session.start(user)

            self.home = HomeWindow(on_logout=self.show_login)
            self.home.show()
            self.close()
        else:
            self.ui.lbl_error.setText("Nome de usuário ou senha inválida. Tente novamente.")
            self.ui.lbl_error.setVisible(True)

    def show_login(self):
        self.show()

    def clear_error(self):
        self.ui.lbl_error.setVisible(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
