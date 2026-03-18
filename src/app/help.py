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

# IMPORT HELP WINDOW
from gui.window.main_window.ui_help_window import UI_HelpWindow
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

# IMPORT SESSION
from auth.session import Session

# HELP WINDOW
class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()

         # ðŸ” Verifica sessÃ£o ANTES de tudo
        if not Session.is_authenticated():
            self.close()
            return
        
        self.user = Session.get()

        # SETUP HELP WINDOW
        self.ui = UI_HelpWindow()
        self.ui.setup_ui(self)

        # botÃ£o voltar
        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)
        self.ui.btn_download.clicked.connect(self.open_manual_link)

        
        print(self.user["username"])
        print(self.user["tag"])

    def go_home(self):
        from home import HomeWindow  # import local evita circular
        self.home = HomeWindow()
        self.home.show()
        self.close()

    def open_profile(self):
        from profile import ProfileWindow
        self.profile = ProfileWindow()
        self.profile.show()
        self.close()

    def open_manual_link(self):
        # Substituir pelo link real do Google Drive
        url = "https://drive.google.com/your-manual-link"
        QDesktopServices.openUrl(QUrl(url))

# Copyright (c) 2026 Raphael da Silva. All rights reserved.

