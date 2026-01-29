"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    Screen to filter materials, requests, actions and employees.
====================================================================
"""

import sys
import os

from qt_core import *

from gui.window.main_window.ui_screen_filter_window import UI_ScreenFilterWindow
from auth.session import Session
from material_service import MaterialService


class ScreenFilterWindow(QMainWindow):
    def __init__(self, category_tag: str):
        super().__init__()

        # -----------------------------
        #  Sessão
        # -----------------------------
        if not Session.is_authenticated():
            self.close()
            return

        self.user = Session.get()

        # Tag vinda da Home (LIM, ELE, HID, FER, AUT, ...)
        self.category_tag = category_tag

        # -----------------------------
        #  UI
        # -----------------------------
        self.ui = UI_ScreenFilterWindow()
        self.ui.setup_ui(self)

        # Página inicial sempre a de materiais
        self.ui.pages_stack.setCurrentWidget(self.ui.page_materials)

        # -----------------------------
        #  Conexões TOP BAR
        # -----------------------------
        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)

        # -----------------------------
        #  Conexões SIDEBAR – CATEGORIA
        #  (troca a tag e recarrega materiais)
        # -----------------------------
        self.ui.btn_cat_limpeza.clicked.connect(
            lambda: self.change_category("LIM")
        )
        self.ui.btn_cat_eletrica.clicked.connect(
            lambda: self.change_category("ELE")
        )
        self.ui.btn_cat_hidraulica.clicked.connect(
            lambda: self.change_category("HID")
        )
        self.ui.btn_cat_ferramentas.clicked.connect(
            lambda: self.change_category("FER")
        )
        self.ui.btn_cat_automoveis.clicked.connect(
            lambda: self.change_category("AUT")
        )

        # -----------------------------
        #  Conexões SIDEBAR – AÇÕES
        # -----------------------------
        # Consultar
        self.ui.btn_sidebar_consultar.clicked.connect(
            lambda: self.ui.pages_stack.setCurrentWidget(self.ui.page_consultar)
        )

        # Solicitar
        self.ui.btn_sidebar_solicitar.clicked.connect(
            lambda: self.ui.pages_stack.setCurrentWidget(self.ui.page_solicitar)
        )

        # Cadastro de Funcionários
        self.ui.btn_sidebar_cad_func.clicked.connect(
            lambda: self.ui.pages_stack.setCurrentWidget(self.ui.page_cad_func)
        )

        # (Relatório / Imprimir / Exportar e Ajuda você liga depois, quando tiver as telas)

        # -----------------------------
        #  BOTÃO FILTRAR MATERIAIS
        # -----------------------------
        self.ui.btn_filter_materials.clicked.connect(self.apply_filters)

        # -----------------------------
        #  PRIMEIRA CARGA DA TABELA
        # -----------------------------
        self.load_materials()

        self.show()

    # ============================================================
    #  CARREGAR / FILTRAR MATERIAIS
    # ============================================================
    def change_category(self, tag: str):
        """
        Chamado quando o usuário clica numa categoria do sidebar.
        Troca a tag e recarrega os materiais.
        """
        self.category_tag = tag
        self.ui.pages_stack.setCurrentWidget(self.ui.page_materials)
        self.load_materials()

    def load_materials(self):
        """
        Carrega os materiais apenas pela categoria (sem filtro de texto).
        """
        rows = MaterialService.get_materials(
            category_tag=self.category_tag,
            description=None,
            item_number=None,
            product=None,
            category=None,
        )
        self.populate_material_table(rows)

    def apply_filters(self):
        """
        Botão FILTRAR da página de materiais.
        Usa os campos do filtro + a tag da categoria.
        """
        description = self.ui.input_description.text().strip()
        item_number = self.ui.input_item_number.text().strip()

        product = self.ui.combo_product.currentText()
        if product == "Selecione":
            product = ""

        category = self.ui.combo_category.currentText()
        if category == "Selecione":
            category = ""

        rows = MaterialService.get_materials(
            category_tag=self.category_tag,
            description=description or None,
            item_number=item_number or None,
            product=product or None,
            category=category or None,
        )
        self.populate_material_table(rows)

    def populate_material_table(self, rows):
        """
        Preenche a tabela de materiais com as linhas vindas do banco.
        Espera-se que cada linha seja:
        (id_item, desceprection, product, category, quantity, unit_measurement)
        """
        table = self.ui.table_materials
        table.setRowCount(0)

        if not rows:
            return

        table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # só leitura
                table.setItem(row_index, col_index, item)

    # ============================================================
    #  NAVEGAÇÃO
    # ============================================================
    def go_home(self):
        from home import HomeWindow
        self.home = HomeWindow()
        self.home.show()
        self.close()

    def open_profile(self):
        from profile import ProfileWindow
        self.profile = ProfileWindow()
        self.profile.show()
        self.close()
