# screen_filter.py

"""
SCREEN FILTER WINDOW CONTROLLER
"""

from qt_core import *
from gui.window.main_window.ui_screen_filter_window import UI_ScreenFilterWindow
from auth.session import Session
from material_service import MaterialService


class ScreenFilterWindow(QMainWindow):
    def __init__(self, category_tag: str):
        super().__init__()

        # --- Sessão ---
        if not Session.is_authenticated():
            self.close()
            return

        self.user = Session.get()
        self.category_tag = category_tag  # "ELE", "HID", "LIM", ...

        # --- UI ---
        self.ui = UI_ScreenFilterWindow()
        self.ui.setup_ui(self)

        # guarda referência da tabela principal de materiais
        # (tanto faz se no UI ela se chama 'table' ou 'table_materials')
        self.table = getattr(self.ui, "table", None)
        if self.table is None:
            self.table = getattr(self.ui, "table_materials", None)

        # idem para o botão FILTRAR
        self.btn_filter = getattr(self.ui, "btn_filter", None)
        if self.btn_filter is None:
            self.btn_filter = getattr(self.ui, "btn_filter_materials", None)

        if self.btn_filter is not None:
            self.btn_filter.clicked.connect(self.apply_filters)

        # botões do topo
        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)

        # se existir botão "Consultar" na sidebar, mostra página de consulta
        btn_sidebar_consultar = getattr(self.ui, "btn_sidebar_consultar", None)
        pages_stack = getattr(self.ui, "pages_stack", None)
        page_consultar = getattr(self.ui, "page_consultar", None)
        if btn_sidebar_consultar and pages_stack and page_consultar:
            btn_sidebar_consultar.clicked.connect(
                lambda: pages_stack.setCurrentWidget(page_consultar)
            )

        # carrega tabela inicial
        self.load_materials()

        self.show()

    # -----------------------------
    #  MAPA TAG -> PREFIXO do id_item
    # -----------------------------
    def get_category_prefix(self) -> str:
        prefix_map = {
            "ELE": "E",   # Elétrica -> E001, E002...
            "HID": "H",   # Hidráulica -> H001...
            "LIM": "L",   # Limpeza...
            "FER": "F",   # Ferramentas...
            "AUT": "A",   # Automóveis...
        }
        return prefix_map.get(self.category_tag, "")

    # -----------------------------
    #  CARREGAR MATERIAIS
    # -----------------------------
    def load_materials(self, description: str = "", id_item: str = "", product: str = ""):
        prefix = self.get_category_prefix()

        rows = MaterialService.get_materials(
            category_prefix=prefix,
            description=description,
            id_item=id_item,
            product=product,
        )

        self.populate_table(rows)

    def populate_table(self, rows):
        """Preenche a tabela de materiais."""
        if self.table is None:
            # segurança: se ainda assim não tiver tabela, não faz nada
            return

        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(r, c, item)

    # -----------------------------
    #  FILTRO (botão FILTRAR)
    # -----------------------------
    def apply_filters(self):
        # tenta pegar os campos do layout; se não existir, usa string vazia
        desc_input = getattr(self.ui, "input_description", None)
        num_input = getattr(self.ui, "input_item_number", None)
        prod_combo = getattr(self.ui, "combo_product", None)

        desc = desc_input.text().strip() if desc_input else ""
        num = num_input.text().strip() if num_input else ""
        prod = ""

        if prod_combo:
            prod = prod_combo.currentText().strip()
            if prod.lower() == "selecione":
                prod = ""

        self.load_materials(description=desc, id_item=num, product=prod)

    # -----------------------------
    #  NAVEGAÇÃO
    # -----------------------------
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
