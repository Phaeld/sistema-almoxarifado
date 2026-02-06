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
from control_gas import ControlGasWindow
from help import HelpWindow

# IMPORT SESSION
from auth.session import Session


# HOME WINDOW
class HomeWindow(QMainWindow):
    def __init__(self, on_logout=None):
        super().__init__()

        self.on_logout = on_logout

        # 🔐 Verifica sessão ANTES de tudo
        if not Session.is_authenticated():
            self.close()
            return

        self.user = Session.get()

        self.ui = UI_HomeWindow()
        self.ui.setup_ui(self)

        self._connect_top_buttons()
        self._connect_cards()

        print(self.user["username"])
        print(self.user["tag"])





    def _connect_top_buttons(self):
        self.ui.btn_sair.clicked.connect(self.logout)
        self.ui.btn_profile.clicked.connect(self.open_profile)

    def _connect_cards(self):
        for card in self.ui.menu_cards:
            card.clicked.connect(self.handle_card_click)


    def handle_card_click(self, tag):
        if tag == "AJU":
            self.open_help()
            return

        if tag == "ABA":
            position = (self.user.get("position") or "").upper()
            if position not in {"ABAST", "ADMIN"}:
                QMessageBox.warning(
                    self,
                    "Acesso negado",
                    "Você não tem permissão para acessar Abastecimento."
                )
                return
            self.open_control_gas()
            return

        if tag == "COL":
            self.open_cad_func()
            return

        supported_tags = {"LIM", "ELE", "HID", "FER", "AUT"}
        if tag in supported_tags:
            self.open_screen_filter(tag)
            return

        QMessageBox.information(
            self,
            "Em desenvolvimento",
            "Esta funcionalidade estará disponível em breve."
        )

    def open_screen_filter(self, tag):
        self.screen_filter = ScreenFilterWindow(tag)
        self.screen_filter.show()
        self.close()

    def open_help(self):
        self.help = HelpWindow()
        self.help.show()
        self.close()
    
    def open_control_gas(self):
        self.control_gas = ControlGasWindow()
        self.control_gas.show()
        self.close()

    def open_cad_func(self):
        self.screen_filter = ScreenFilterWindow("LIM")
        self.screen_filter.show()
        self.screen_filter.show_cad_func_page()
        self.close()

    def open_profile(self):
        from profile import ProfileWindow
        self.profile = ProfileWindow()
        self.profile.show()
        self.close()

    # LOGOUT
    def logout(self):
        Session.end()

        if self.on_logout:
            self.on_logout()

        self.close()
