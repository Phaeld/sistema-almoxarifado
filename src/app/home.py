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

# IMPORT HOME WINDOW AND SCREEN FILTER
from gui.window.main_window.ui_home_window import UI_HomeWindow
from screen_filter import ScreenFilterWindow
from help import HelpWindow

# HOME WINDOW
class HomeWindow(QMainWindow):
    def __init__(self, on_logout=None):
        super().__init__()

        self.on_logout = on_logout

        self.ui = UI_HomeWindow()
        self.ui.setup_ui(self)

        self._connect_top_buttons()
        self._connect_cards()


    def _connect_top_buttons(self):
        self.ui.btn_sair.clicked.connect(self.logout)
        self.ui.btn_perfil.clicked.connect(
            lambda: self.open_screen_filter("PER")
        )

    def _connect_cards(self):
        for card in self.ui.menu_cards:
            card.clicked.connect(self.handle_card_click)


    def handle_card_click(self, tag):
        if tag == "AJU":
            self.open_help()
        else:
            self.open_screen_filter(tag)

    def open_screen_filter(self, tag):
        self.screen_filter = ScreenFilterWindow(tag)
        self.screen_filter.show()
        self.close()

    def open_help(self):
        self.help = HelpWindow()
        self.help.show()
        self.close()

    # LOGOUT
    def logout(self):
        if self.on_logout:
            self.on_logout()
        self.close()