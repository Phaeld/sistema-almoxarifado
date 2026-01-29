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

        # ---------- Sessão ----------
        if not Session.is_authenticated():
            self.close()
            return

        self.user = Session.get()
        self.category_tag = category_tag  # "ELE", "HID", "LIM", ...

        # ---------- UI ----------
        self.ui = UI_ScreenFilterWindow()
        self.ui.setup_ui(self)

        # Referência da tabela principal
        self.table = self.ui.table_materials

        # Botão FILTRAR
        self.ui.btn_filter.clicked.connect(self.apply_filters)

        # Top bar
        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)

        # Sidebar categorias -> mudam o prefixo e recarregam a tabela
        self.ui.btn_cat_limpeza.clicked.connect(lambda: self.change_category("LIM"))
        self.ui.btn_cat_eletrica.clicked.connect(lambda: self.change_category("ELE"))
        self.ui.btn_cat_hidraulica.clicked.connect(lambda: self.change_category("HID"))
        self.ui.btn_cat_ferramentas.clicked.connect(lambda: self.change_category("FER"))
        self.ui.btn_cat_automoveis.clicked.connect(lambda: self.change_category("AUT"))
        self.ui.btn_cat_abastecimento.clicked.connect(lambda: self.change_category("ABA"))

        # (No futuro) botões de ações: consultar/solicitar/etc.
        # self.ui.btn_sidebar_consultar.clicked.connect(...)
        # self.ui.btn_sidebar_solicitar.clicked.connect(...)

        # Carrega lista inicial com base na categoria que veio da Home
        self.load_materials()

        self.show()

    # -------------------------------------------------
    #  MAPA TAG -> PREFIXO (id_item)
    # -------------------------------------------------
    def get_category_prefix(self) -> str:
        prefix_map = {
            "ELE": "E",   # Elétrica
            "HID": "H",   # Hidráulica
            "LIM": "L",   # Limpeza
            "FER": "F",   # Ferramentas
            "AUT": "A",   # Automóveis
            "ABA": "G",   # Abastecimento (ex.: G001...)
        }
        return prefix_map.get(self.category_tag, "")

    # -------------------------------------------------
    #  TROCA CATEGORIA PELO SIDEBAR
    # -------------------------------------------------
    def change_category(self, new_tag: str):
        self.category_tag = new_tag
        # zera filtros de texto para não confundir
        self.ui.input_description.clear()
        self.ui.input_item_number.clear()
        self.ui.combo_product.setCurrentIndex(0)
        self.ui.combo_category.setCurrentIndex(0)
        self.load_materials()

    # -------------------------------------------------
    #  CARREGAR MATERIAIS
    # -------------------------------------------------
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
        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(r, c, item)

    # -------------------------------------------------
    #  FILTRO (botão FILTRAR)
    # -------------------------------------------------
    def apply_filters(self):
        desc = self.ui.input_description.text().strip()
        num = self.ui.input_item_number.text().strip()

        prod = self.ui.combo_product.currentText().strip()
        if prod.lower() == "selecione":
            prod = ""

        # (opcional) você pode usar também a categoria selecionada
        # category_text = self.ui.combo_category.currentText().strip()
        # se quiser um filtro extra, é só adaptar o MaterialService

        self.load_materials(description=desc, id_item=num, product=prod)

    # -------------------------------------------------
    #  NAVEGAÇÃO
    # -------------------------------------------------
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
