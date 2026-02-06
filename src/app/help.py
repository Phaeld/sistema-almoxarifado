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

         # 🔐 Verifica sessão ANTES de tudo
        if not Session.is_authenticated():
            self.close()
            return
        
        self.user = Session.get()

        # SETUP HELP WINDOW
        self.ui = UI_HelpWindow()
        self.ui.setup_ui(self)

        # botão voltar
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
