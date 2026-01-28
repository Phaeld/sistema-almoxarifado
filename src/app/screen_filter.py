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

# IMPORT SCREEN FILTER WINDOW (UI)
from gui.window.main_window.ui_screen_filter_window import UI_ScreenFilterWindow

# IMPORT SESSION
from auth.session import Session


# SCREEN FILTER WINDOW (CONTROLLER)
class ScreenFilterWindow(QMainWindow):
    def __init__(self, category_tag):
        super().__init__()

        # 🔐 Verifica sessão ANTES de tudo
        if not Session.is_authenticated():
            self.close()
            return

        self.user = Session.get()
        self.category = category_tag   # ex.: "ELE", "HID", "CONSULT", etc
        print("Categoria selecionada:", self.category)

        # ---------- SETUP UI ----------
        self.ui = UI_ScreenFilterWindow()
        self.ui.setup_ui(self)

        # ---------- TOP BAR ----------
        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)

        # ---------- SIDEBAR: troca de páginas ----------
        # Página padrão: materiais (categorias)
        initial_page = self.ui.page_materials

        # Se quiser no futuro abrir direto em outra página via tag:
        if self.category == "CONSULT":
            initial_page = self.ui.page_consultar
        elif self.category == "SOLIC":
            initial_page = self.ui.page_solicitar
        elif self.category == "STAFF":
            initial_page = self.ui.page_staff

        self.ui.pages_stack.setCurrentWidget(initial_page)

        # Botões do sidebar
        self.ui.btn_sidebar_consultar.clicked.connect(
            lambda: self.ui.pages_stack.setCurrentWidget(self.ui.page_consultar)
        )
        self.ui.btn_sidebar_solicitar.clicked.connect(
            lambda: self.ui.pages_stack.setCurrentWidget(self.ui.page_solicitar)
        )
        self.ui.btn_sidebar_staff.clicked.connect(
            lambda: self.ui.pages_stack.setCurrentWidget(self.ui.page_staff)
        )
        # Se quiser, pode deixar o de materiais também (categoria padrão)
        # por exemplo quando clicar em alguma categoria:
        # self.ui.btn_sidebar_alguma_coisa.clicked.connect(
        #     lambda: self.ui.pages_stack.setCurrentWidget(self.ui.page_materials)
        # )

        # Debug da sessão (só pra conferir)
        print(self.user["username"])
        print(self.user.get("tag"))

        # MOSTRA JANELA
        self.show()

    # =============================
    # NAVEGAÇÃO
    # =============================
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


# Teste isolado (normalmente não usa porque quem abre é o Home)
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = ScreenFilterWindow("ELE")
#     sys.exit(app.exec())
