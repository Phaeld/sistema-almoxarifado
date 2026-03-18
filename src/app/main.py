# ============================================================================
# Author: Raphael da Silva
# Copyright (c) 2026 Raphael da Silva. All rights reserved.
# Proprietary and confidential software.
# Unauthorized use, copying, modification, distribution, disclosure,
# reverse engineering, sublicensing, or commercialization of this source code,
# in whole or in part, is strictly prohibited without prior written permission.
# This work is protected under Brazilian Software Law (Law No. 9,609/1998),
# Brazilian Copyright Law (Law No. 9,610/1998), and other applicable laws.
# ============================================================================


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
from log_service import LogService



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
            LogService.log_event("LOGIN_SUCCESS", "Login realizado com sucesso.", user)

            self.home = HomeWindow(on_logout=self.show_login)
            self.home.show()
            self.close()
        else:
            self.ui.lbl_error.setText("Nome de usuÃ¡rio ou senha invÃ¡lida. Tente novamente.")
            self.ui.lbl_error.setVisible(True)
            LogService.log_event("LOGIN_FAILED", f"Tentativa de login para usuario={username}.", {"username": username})

    def show_login(self):
        self.show()

    def clear_error(self):
        self.ui.lbl_error.setVisible(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())





# Copyright (c) 2026 Raphael da Silva. All rights reserved.

