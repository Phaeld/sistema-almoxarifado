"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    Internal warehouse management system with graphical interface.
====================================================================
"""

from qt_core import *
from gui import resources_rc   # garante que os ícones do .qrc sejam carregados


class UI_ScreenFilterWindow(object):

    def setup_ui(self, parent: QMainWindow):
        if not parent.objectName():
            parent.setObjectName("ScreenFilterWindow")

        # =============================
        #  WINDOW
        # =============================
        parent.resize(1200, 720)
        parent.setMinimumSize(960, 540)
        parent.setWindowTitle("Almoxarifado Obras - Filtros, Pedidos e Consultas")
        parent.setWindowIcon(QIcon("assets/icon.jpg"))
        parent.setStyleSheet("background-color: #E8E2EE;")

        # CENTRAL
        self.central_widget = QWidget(parent)
        parent.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =============================
        #  TOP BAR
        # =============================
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(50)
        self.top_bar.setStyleSheet("background-color: #390E68;")

        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)

        self.btn_home = QPushButton("  Inicial")
        self.btn_home.setIcon(QIcon("assets/home.png"))
        self.btn_home.setStyleSheet(self._top_button_style())

        self.btn_profile = QPushButton("  Meu perfil")
        self.btn_profile.setIcon(QIcon("assets/user_profile.png"))
        self.btn_profile.setStyleSheet(self._top_button_style())

        top_layout.addWidget(self.btn_home)
        top_layout.addStretch()
        top_layout.addWidget(self.btn_profile)

        main_layout.addWidget(self.top_bar)

        # =============================
        #  BODY (SIDEBAR + CONTENT)
        # =============================
        body = QFrame()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # ---------- SIDEBAR ----------
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(300)
        self.sidebar.setStyleSheet("background-color: #B6A8C9;")

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(10)

        # CATEGORIA
        sidebar_layout.addWidget(self._section_title("CATEGORIA"))

        self.btn_cat_limpeza = self._sidebar_button("assets/clear.png",
                                                    "Limpeza, Higiene e Alimentos")
        self.btn_cat_eletrica = self._sidebar_button("assets/electrical.png", "Elétrica")
        self.btn_cat_hidraulica = self._sidebar_button("assets/hydraulic_water.png", "Hidráulica")
        self.btn_cat_ferramentas = self._sidebar_button("assets/settings_tools.png",
                                                        "Ferramentas Gerais")
        self.btn_cat_automoveis = self._sidebar_button("assets/truck.png", "Automóveis")

        sidebar_layout.addWidget(self.btn_cat_limpeza)
        sidebar_layout.addWidget(self.btn_cat_eletrica)
        sidebar_layout.addWidget(self.btn_cat_hidraulica)
        sidebar_layout.addWidget(self.btn_cat_ferramentas)
        sidebar_layout.addWidget(self.btn_cat_automoveis)

        sidebar_layout.addWidget(self._hr_line())

        # AÇÕES
        sidebar_layout.addWidget(self._section_title("AÇÕES"))

        self.btn_sidebar_consultar = self._sidebar_button("assets/magnifier.png", "Consultar")
        self.btn_sidebar_solicitar = self._sidebar_button("assets/request.png", "Solicitar")
        self.btn_sidebar_relatorio = self._sidebar_button("assets/graphic.png", "Relatório")
        self.btn_sidebar_imprimir = self._sidebar_button("assets/print.png", "Imprimir")
        self.btn_sidebar_exportar = self._sidebar_button("assets/export.png", "Exportar")

        sidebar_layout.addWidget(self.btn_sidebar_consultar)
        sidebar_layout.addWidget(self.btn_sidebar_solicitar)
        sidebar_layout.addWidget(self.btn_sidebar_relatorio)
        sidebar_layout.addWidget(self.btn_sidebar_imprimir)
        sidebar_layout.addWidget(self.btn_sidebar_exportar)

        sidebar_layout.addWidget(self._hr_line())

        # OUTROS
        sidebar_layout.addWidget(self._section_title("OUTROS"))

        self.btn_sidebar_cad_func = self._sidebar_button(
            "assets/database_icon.png", "Cadastros dos Funcionários"
        )
        self.btn_sidebar_ajuda = self._sidebar_button(
            "assets/help_software.png", "Ajuda"
        )

        sidebar_layout.addWidget(self.btn_sidebar_cad_func)
        sidebar_layout.addWidget(self.btn_sidebar_ajuda)

        sidebar_layout.addStretch()

        # ---------- CONTENT ----------
        self.content = QFrame()
        self.content.setStyleSheet("background-color: #EDE7F2;")

        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(30, 25, 30, 25)
        content_layout.setSpacing(20)

        # STACK DE PÁGINAS
        self.pages_stack = QStackedWidget()
        content_layout.addWidget(self.pages_stack)

        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.content)

        main_layout.addWidget(body)

        # =============================
        #  PÁGINAS
        # =============================
        self.page_materials = self._build_page_materials()
        self.page_consultar = self._build_page_consultar()
        self.page_solicitar = self._build_page_solicitar()
        self.page_relatorio = self._build_page_relatorio()
        self.page_cad_func = self._build_page_cad_func()

        self.pages_stack.addWidget(self.page_materials)
        self.pages_stack.addWidget(self.page_consultar)
        self.pages_stack.addWidget(self.page_solicitar)
        self.pages_stack.addWidget(self.page_relatorio)
        self.pages_stack.addWidget(self.page_cad_func)

        # Página inicial padrão: materiais
        self.pages_stack.setCurrentWidget(self.page_materials)

    # ============================================================
    #  PÁGINA 1 – FILTRO DE MATERIAIS
    # ============================================================
    def _build_page_materials(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)

        # CARD DE FILTRO
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #DDD4E6;
                border-radius: 10px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(12)

        title = QLabel("FILTRO - Materiais")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #3E0F63;
            }
        """)
        card_layout.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(10)

        label_style = """
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #3A1A5E;
            }
        """
        line_style = """
            QLineEdit {
                background-color: #E8E2EE;
                border-radius: 6px;
                padding: 6px 10px;
                border: 1px solid #C7B7DF;
                color: #3A1A5E;
            }
        """
        combo_style = """
            QComboBox {
                background-color: #E8E2EE;
                border-radius: 6px;
                padding: 4px 10px;
                border: 1px solid #C7B7DF;
                color: #3A1A5E;
            }
        """

        # Descrição
        lbl_desc = QLabel("Descrição")
        lbl_desc.setStyleSheet(label_style)
        self.input_description = QLineEdit()
        self.input_description.setPlaceholderText("Descrição")
        self.input_description.setStyleSheet(line_style)

        # Número Item
        lbl_num = QLabel("Número Item")
        lbl_num.setStyleSheet(label_style)
        self.input_item_number = QLineEdit()
        self.input_item_number.setPlaceholderText("Número Item")
        self.input_item_number.setStyleSheet(line_style)

        # Categoria
        lbl_cat = QLabel("Categoria")
        lbl_cat.setStyleSheet(label_style)
        self.combo_category = QComboBox()
        self.combo_category.setStyleSheet(combo_style)
        self.combo_category.addItem("Selecione")
        # TODO: preencher categorias via banco ou código
        # self.combo_category.addItems(["ELÉTRICA", "HIDRÁULICA", ...])

        # Produto
        lbl_prod = QLabel("Produto")
        lbl_prod.setStyleSheet(label_style)
        self.combo_product = QComboBox()
        self.combo_product.setStyleSheet(combo_style)
        self.combo_product.addItem("Selecione")
        # TODO: preencher produtos via banco
        # self.combo_product.addItems(["Disjuntor", "Relé", ...])

        # Botão Filtrar
        self.btn_filter_materials = QPushButton("FILTRAR")
        self.btn_filter_materials.setFixedHeight(40)
        self.btn_filter_materials.setStyleSheet(self._primary_button())

        grid.addWidget(lbl_desc, 0, 0)
        grid.addWidget(self.input_description, 1, 0)

        grid.addWidget(lbl_num, 0, 1)
        grid.addWidget(self.input_item_number, 1, 1)

        grid.addWidget(lbl_cat, 0, 2)
        grid.addWidget(self.combo_category, 1, 2)

        grid.addWidget(lbl_prod, 2, 0)
        grid.addWidget(self.combo_product, 3, 0)

        grid.addWidget(self.btn_filter_materials, 3, 2, alignment=Qt.AlignRight)

        card_layout.addLayout(grid)
        layout.addWidget(card)

        # TABELA DE MATERIAIS
        self.table_materials = QTableWidget()
        self.table_materials.setColumnCount(6)
        self.table_materials.setHorizontalHeaderLabels([
            "Nm item", "Descrição", "Produto",
            "Categoria", "Quantidade", "Un. medida"
        ])
        self._style_table(self.table_materials)

        layout.addWidget(self.table_materials)
        return page

    # ============================================================
    #  PÁGINA 2 – CONSULTAR AÇÕES
    # ============================================================
    def _build_page_consultar(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #DDD4E6;
                border-radius: 10px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(12)

        title = QLabel("FILTRO - Consultar")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #3E0F63;
            }
        """)
        card_layout.addWidget(title)

        label_style = """
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #3A1A5E;
            }
        """
        line_style = """
            QLineEdit {
                background-color: #E8E2EE;
                border-radius: 6px;
                padding: 6px 10px;
                border: 1px solid #C7B7DF;
                color: #3A1A5E;
            }
        """
        combo_style = """
            QComboBox {
                background-color: #E8E2EE;
                border-radius: 6px;
                padding: 4px 10px;
                border: 1px solid #C7B7DF;
                color: #3A1A5E;
            }
        """

        grid = QGridLayout()
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(10)

        # Assunto
        lbl_ass = QLabel("Assunto")
        lbl_ass.setStyleSheet(label_style)
        self.cons_input_subject = QLineEdit()
        self.cons_input_subject.setStyleSheet(line_style)

        # Número Ação
        lbl_num = QLabel("Número Ação")
        lbl_num.setStyleSheet(label_style)
        self.cons_input_action = QLineEdit()
        self.cons_input_action.setStyleSheet(line_style)

        # Tipo
        lbl_tipo = QLabel("Tipo")
        lbl_tipo.setStyleSheet(label_style)
        self.cons_combo_type = QComboBox()
        self.cons_combo_type.setStyleSheet(combo_style)
        self.cons_combo_type.addItem("Selecione")
        # TODO: preencher tipos de ação

        # Produto
        lbl_prod = QLabel("Produto")
        lbl_prod.setStyleSheet(label_style)
        self.cons_combo_product = QComboBox()
        self.cons_combo_product.setStyleSheet(combo_style)
        self.cons_combo_product.addItem("Selecione")
        # TODO: preencher

        # Observação
        lbl_obs = QLabel("Observação")
        lbl_obs.setStyleSheet(label_style)
        self.cons_input_obs = QLineEdit()
        self.cons_input_obs.setStyleSheet(line_style)

        # Data
        lbl_data = QLabel("Data")
        lbl_data.setStyleSheet(label_style)
        self.cons_input_date = QLineEdit()
        self.cons_input_date.setPlaceholderText("dd/mm/aaaa")
        self.cons_input_date.setStyleSheet(line_style)

        # Botão
        self.btn_filter_consult = QPushButton("FILTRAR")
        self.btn_filter_consult.setFixedHeight(40)
        self.btn_filter_consult.setStyleSheet(self._primary_button())

        grid.addWidget(lbl_ass, 0, 0)
        grid.addWidget(self.cons_input_subject, 1, 0)

        grid.addWidget(lbl_num, 0, 1)
        grid.addWidget(self.cons_input_action, 1, 1)

        grid.addWidget(lbl_tipo, 0, 2)
        grid.addWidget(self.cons_combo_type, 1, 2)

        grid.addWidget(lbl_prod, 2, 0)
        grid.addWidget(self.cons_combo_product, 3, 0)

        grid.addWidget(lbl_obs, 2, 1)
        grid.addWidget(self.cons_input_obs, 3, 1)

        grid.addWidget(lbl_data, 2, 2)
        grid.addWidget(self.cons_input_date, 3, 2)

        grid.addWidget(self.btn_filter_consult, 4, 2, alignment=Qt.AlignRight)

        card_layout.addLayout(grid)
        layout.addWidget(card)

        # TABELA CONSULTA
        self.table_consult = QTableWidget()
        self.table_consult.setColumnCount(6)
        self.table_consult.setHorizontalHeaderLabels([
            "Nm_ação", "Assunto", "Obs",
            "Categoria", "Permitido por", "Data"
        ])
        self._style_table(self.table_consult)

        layout.addWidget(self.table_consult)
        return page

    # ============================================================
    #  PÁGINA 3 – SOLICITAR MATERIAIS
    # ============================================================
    def _build_page_solicitar(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #DDD4E6;
                border-radius: 10px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(12)

        self.req_title = QLabel("TABELA - Solicitar")
        self.req_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #3E0F63;
            }
        """)
        card_layout.addWidget(self.req_title)

        label_style = """
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #3A1A5E;
            }
        """
        line_style = """
            QLineEdit {
                background-color: #E8E2EE;
                border-radius: 6px;
                padding: 6px 10px;
                border: 1px solid #C7B7DF;
                color: #3A1A5E;
            }
        """
        combo_style = """
            QComboBox {
                background-color: #E8E2EE;
                border-radius: 6px;
                padding: 4px 10px;
                border: 1px solid #C7B7DF;
                color: #3A1A5E;
            }
        """

        grid = QGridLayout()
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(10)

        # Categoria
        lbl_cat = QLabel("Categoria")
        lbl_cat.setStyleSheet(label_style)
        self.req_combo_category = QComboBox()
        self.req_combo_category.setStyleSheet(combo_style)
        self.req_combo_category.addItem("Selecione")

        # Tipo Solicitação
        lbl_tipo = QLabel("Tipo Solicitação")
        lbl_tipo.setStyleSheet(label_style)
        self.req_combo_type = QComboBox()
        self.req_combo_type.setStyleSheet(combo_style)
        self.req_combo_type.addItem("Selecione")

        # Descrição
        lbl_desc = QLabel("Descrição")
        lbl_desc.setStyleSheet(label_style)
        self.req_input_description = QLineEdit()
        self.req_input_description.setStyleSheet(line_style)

        grid.addWidget(lbl_cat, 0, 0)
        grid.addWidget(self.req_combo_category, 1, 0)

        grid.addWidget(lbl_tipo, 0, 2)
        grid.addWidget(self.req_combo_type, 1, 2)

        grid.addWidget(lbl_desc, 2, 0, 1, 3)
        grid.addWidget(self.req_input_description, 3, 0, 1, 3)

        card_layout.addLayout(grid)

        # TABELA DE ITENS
        lbl_itens = QLabel("Itens")
        lbl_itens.setStyleSheet(label_style)
        items_header = QHBoxLayout()
        items_header.addWidget(lbl_itens)
        items_header.addStretch()
        self.btn_add_material = QPushButton("CADASTRAR ITEM")
        self.btn_add_material.setStyleSheet(self._secondary_button())
        items_header.addWidget(self.btn_add_material)
        card_layout.addLayout(items_header)

        self.table_request_items = QTableWidget()
        self.table_request_items.setColumnCount(4)
        self.table_request_items.setHorizontalHeaderLabels([
            "Add", "Número Item", "Descrição Item", "Quantidade"
        ])
        self._style_table(self.table_request_items)

        card_layout.addWidget(self.table_request_items)

        # Campos inferiores
        bottom_grid = QGridLayout()
        bottom_grid.setHorizontalSpacing(30)
        bottom_grid.setVerticalSpacing(10)

        lbl_solic = QLabel("Solicitado por")
        lbl_solic.setStyleSheet(label_style)
        self.req_input_requested_by = QLineEdit()
        self.req_input_requested_by.setStyleSheet(line_style)

        lbl_obs = QLabel("Observações adicionais (opcional)")
        lbl_obs.setStyleSheet(label_style)
        self.req_input_obs = QTextEdit()
        self.req_input_obs.setStyleSheet("""
            QTextEdit {
                background-color: #E8E2EE;
                border-radius: 6px;
                border: 1px solid #C7B7DF;
                color: #3A1A5E;
                padding: 6px 10px;
            }
        """)

        lbl_aut = QLabel("Autorizado por")
        lbl_aut.setStyleSheet(label_style)
        self.req_combo_authorized = QComboBox()
        self.req_combo_authorized.setStyleSheet(combo_style)
        self.req_combo_authorized.addItem("Selecione")

        bottom_grid.addWidget(lbl_solic, 0, 0)
        bottom_grid.addWidget(self.req_input_requested_by, 1, 0)

        bottom_grid.addWidget(lbl_obs, 0, 1)
        bottom_grid.addWidget(self.req_input_obs, 1, 1, 3, 1)

        bottom_grid.addWidget(lbl_aut, 2, 0)
        bottom_grid.addWidget(self.req_combo_authorized, 3, 0)

        card_layout.addLayout(bottom_grid)

        # Botões
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_req_cancel = QPushButton("CANCELAR")
        self.btn_req_cancel.setStyleSheet(self._secondary_button())

        self.btn_req_clear = QPushButton("LIMPAR")
        self.btn_req_clear.setStyleSheet(self._light_button())

        self.btn_req_confirm = QPushButton("CONFIRMAR")
        self.btn_req_confirm.setStyleSheet(self._primary_button())

        btn_row.addWidget(self.btn_req_cancel)
        btn_row.addWidget(self.btn_req_clear)
        btn_row.addWidget(self.btn_req_confirm)

        card_layout.addLayout(btn_row)

        layout.addWidget(card)
        return page

    # ============================================================
    #  PÁGINA 4 – RELATÓRIO (DASHBOARD)
    # ============================================================
    def _build_page_relatorio(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)

        # HEADER FILTERS
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #DDD4E6;
                border-radius: 10px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(12)

        title = QLabel("DASHBOARD – Relatório")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #3E0F63;
            }
        """)
        card_layout.addWidget(title)

        label_style = """
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #3A1A5E;
            }
        """
        combo_style = """
            QComboBox {
                background-color: #E8E2EE;
                border-radius: 6px;
                padding: 4px 10px;
                border: 1px solid #C7B7DF;
                color: #3A1A5E;
            }
        """

        grid = QGridLayout()
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(10)

        lbl_month = QLabel("Meses")
        lbl_month.setStyleSheet(label_style)
        self.report_combo_month = QComboBox()
        self.report_combo_month.setStyleSheet(combo_style)

        lbl_cat = QLabel("Categoria")
        lbl_cat.setStyleSheet(label_style)
        self.report_combo_category = QComboBox()
        self.report_combo_category.setStyleSheet(combo_style)

        lbl_type = QLabel("Tipo")
        lbl_type.setStyleSheet(label_style)
        self.report_combo_type = QComboBox()
        self.report_combo_type.setStyleSheet(combo_style)

        grid.addWidget(lbl_month, 0, 0)
        grid.addWidget(self.report_combo_month, 1, 0)
        grid.addWidget(lbl_cat, 0, 1)
        grid.addWidget(self.report_combo_category, 1, 1)
        grid.addWidget(lbl_type, 0, 2)
        grid.addWidget(self.report_combo_type, 1, 2)

        card_layout.addLayout(grid)
        layout.addWidget(card)

        # METRICS ROW
        metrics = QHBoxLayout()
        metrics.setSpacing(15)

        def metric_card(title_text, value_label_ref):
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: #B8A9C9;
                    border-radius: 10px;
                }
            """)
            l = QVBoxLayout(frame)
            l.setContentsMargins(18, 14, 18, 14)
            t = QLabel(title_text)
            t.setStyleSheet("font-size: 12px; font-weight: bold; color: white;")
            v = QLabel("0")
            v.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
            l.addWidget(v)
            l.addWidget(t)
            return frame, v

        card_total, self.lbl_total_items = metric_card("QNT. TOTAL DE ITENS", None)
        card_out, self.lbl_items_out = metric_card("QNT. ITENS SAIU", None)
        card_in, self.lbl_items_in = metric_card("QNT. ITENS CHEGOU", None)

        stock_frame = QFrame()
        stock_frame.setStyleSheet("""
            QFrame {
                background-color: #B8A9C9;
                border-radius: 10px;
            }
        """)
        stock_layout = QVBoxLayout(stock_frame)
        stock_layout.setContentsMargins(18, 14, 18, 14)
        self.lbl_stock_item = QLabel("-")
        self.lbl_stock_item.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        stock_title = QLabel("ITEM MAIS BAIXO ESTOQUE")
        stock_title.setStyleSheet("font-size: 12px; font-weight: bold; color: white;")
        stock_layout.addWidget(self.lbl_stock_item)
        stock_layout.addWidget(stock_title)

        metrics.addWidget(card_total)
        metrics.addWidget(card_out)
        metrics.addWidget(card_in)
        metrics.addWidget(stock_frame)

        layout.addLayout(metrics)

        # CHART + TOP ITEMS
        content = QHBoxLayout()
        content.setSpacing(15)

        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            QFrame {
                background-color: #B8A9C9;
                border-radius: 10px;
            }
        """)
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(16, 12, 16, 12)
        chart_layout.setSpacing(8)

        chart_title_row = QHBoxLayout()
        self.report_chart_title = QLabel("QNT. ITENS RETIRADOS NA SEMANA")
        self.report_chart_title.setStyleSheet("font-size: 12px; font-weight: bold; color: white;")
        chart_title_row.addWidget(self.report_chart_title)
        chart_title_row.addStretch()

        lbl_period = QLabel("Período")
        lbl_period.setStyleSheet("font-size: 12px; font-weight: bold; color: white;")
        self.report_combo_period = QComboBox()
        self.report_combo_period.setStyleSheet(combo_style)
        chart_title_row.addWidget(lbl_period)
        chart_title_row.addWidget(self.report_combo_period)
        chart_layout.addLayout(chart_title_row)

        self.report_chart = QLabel()
        self.report_chart.setMinimumSize(520, 260)
        self.report_chart.setStyleSheet("""
            QLabel {
                background-color: #D9CEE6;
                border-radius: 8px;
            }
        """)
        self.report_chart.setAlignment(Qt.AlignCenter)
        chart_layout.addWidget(self.report_chart)

        top_frame = QFrame()
        top_frame.setStyleSheet("""
            QFrame {
                background-color: #B8A9C9;
                border-radius: 10px;
            }
        """)
        top_layout = QVBoxLayout(top_frame)
        top_layout.setContentsMargins(16, 12, 16, 12)
        top_layout.setSpacing(8)

        self.report_top_title = QLabel("ITENS MAIS SÃO RETIRADOS")
        self.report_top_title.setStyleSheet("font-size: 12px; font-weight: bold; color: white;")
        top_layout.addWidget(self.report_top_title)

        self.report_top_items = QTableWidget()
        self.report_top_items.setColumnCount(1)
        self.report_top_items.setHorizontalHeaderLabels(["Itens"])
        self.report_top_items.horizontalHeader().setStretchLastSection(True)
        self.report_top_items.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.report_top_items.verticalHeader().setVisible(False)
        self.report_top_items.setAlternatingRowColors(True)
        self.report_top_items.setStyleSheet("""
            QTableWidget {
                background-color: #F6F1FA;
                gridline-color: #CBB2E6;
                color: #3A1A5E;
            }
            QHeaderView::section {
                background-color: #9B3D97;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border: none;
                padding: 6px;
            }
        """)
        top_layout.addWidget(self.report_top_items)

        content.addWidget(chart_frame, stretch=3)
        content.addWidget(top_frame, stretch=1)

        layout.addLayout(content)
        return page

    # ============================================================
    #  PÁGINA 4 – CADASTRO DE FUNCIONÁRIOS
    # ============================================================
    def _build_page_cad_func(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #DDD4E6;
                border-radius: 10px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(12)

        title = QLabel("TABELA – Cadastro dos Funcionários")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #3E0F63;
            }
        """)
        card_layout.addWidget(title)

        label_style = """
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #3A1A5E;
            }
        """
        line_style = """
            QLineEdit {
                background-color: #E8E2EE;
                border-radius: 6px;
                padding: 6px 10px;
                border: 1px solid #C7B7DF;
                color: #3A1A5E;
            }
        """
        combo_style = """
            QComboBox {
                background-color: #E8E2EE;
                border-radius: 6px;
                padding: 4px 10px;
                border: 1px solid #C7B7DF;
                color: #3A1A5E;
            }
        """

        grid = QGridLayout()
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(12)

        # Nome usuário
        lbl_user = QLabel("Nome Usuário")
        lbl_user.setStyleSheet(label_style)
        self.emp_input_username = QLineEdit()
        self.emp_input_username.setStyleSheet(line_style)

        # Nome completo
        lbl_name = QLabel("Nome Completo")
        lbl_name.setStyleSheet(label_style)
        self.emp_input_fullname = QLineEdit()
        self.emp_input_fullname.setStyleSheet(line_style)

        # Nível
        lbl_nivel = QLabel("Nível")
        lbl_nivel.setStyleSheet(label_style)
        self.emp_combo_level = QComboBox()
        self.emp_combo_level.setStyleSheet(combo_style)
        self.emp_combo_level.addItem("Selecione")

        # Cargo
        lbl_cargo = QLabel("Cargo")
        lbl_cargo.setStyleSheet(label_style)
        self.emp_combo_position = QComboBox()
        self.emp_combo_position.setStyleSheet(combo_style)
        self.emp_combo_position.addItem("Selecione")

        # Sessão
        lbl_sessao = QLabel("Sessão")
        lbl_sessao.setStyleSheet(label_style)
        self.emp_input_session = QLineEdit()
        self.emp_input_session.setStyleSheet(line_style)

        # Senha
        lbl_senha = QLabel("Senha")
        lbl_senha.setStyleSheet(label_style)
        self.emp_input_password = QLineEdit()
        self.emp_input_password.setEchoMode(QLineEdit.Password)
        self.emp_input_password.setStyleSheet(line_style)

        # Confirmar senha
        lbl_conf = QLabel("Confirma Senha")
        lbl_conf.setStyleSheet(label_style)
        self.emp_input_confirm = QLineEdit()
        self.emp_input_confirm.setEchoMode(QLineEdit.Password)
        self.emp_input_confirm.setStyleSheet(line_style)

        grid.addWidget(lbl_user, 0, 0)
        grid.addWidget(self.emp_input_username, 1, 0)

        grid.addWidget(lbl_name, 0, 2)
        grid.addWidget(self.emp_input_fullname, 1, 2)

        grid.addWidget(lbl_nivel, 2, 0)
        grid.addWidget(self.emp_combo_level, 3, 0)

        grid.addWidget(lbl_cargo, 2, 1)
        grid.addWidget(self.emp_combo_position, 3, 1)

        grid.addWidget(lbl_sessao, 2, 2)
        grid.addWidget(self.emp_input_session, 3, 2)

        grid.addWidget(lbl_senha, 4, 0)
        grid.addWidget(self.emp_input_password, 5, 0, 1, 2)

        grid.addWidget(lbl_conf, 4, 2)
        grid.addWidget(self.emp_input_confirm, 5, 2)

        card_layout.addLayout(grid)

        # Botões
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_emp_list = QPushButton("EXIBIR COLABORADORES")
        self.btn_emp_list.setStyleSheet(self._light_button())

        self.btn_emp_cancel = QPushButton("CANCELAR")
        self.btn_emp_cancel.setStyleSheet(self._secondary_button())

        self.btn_emp_clear = QPushButton("LIMPAR")
        self.btn_emp_clear.setStyleSheet(self._light_button())

        self.btn_emp_register = QPushButton("CADASTRAR")
        self.btn_emp_register.setStyleSheet(self._primary_button())

        btn_row.addWidget(self.btn_emp_list)
        btn_row.addWidget(self.btn_emp_cancel)
        btn_row.addWidget(self.btn_emp_clear)
        btn_row.addWidget(self.btn_emp_register)

        card_layout.addLayout(btn_row)

        layout.addWidget(card)
        return page

    # ============================================================
    #  ESTILOS / COMPONENTES AUXILIARES
    # ============================================================
    def _style_table(self, table: QTableWidget):
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #F8F3FF;
                gridline-color: #CBB2E6;
                color: #3A1A5E;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #3E0F63;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border: none;
                padding: 6px;
            }
        """)

    def _top_button_style(self) -> str:
        return """
            QPushButton {
                color: white;
                font-size: 16px;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                color: #E0C8FF;
            }
        """

    def _primary_button(self) -> str:
        return """
            QPushButton {
                background-color: #3E0F63;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 18px;
                padding: 8px 26px;
            }
            QPushButton:hover {
                background-color: #53207E;
            }
        """

    def _secondary_button(self) -> str:
        return """
            QPushButton {
                background-color: #B5B1C2;
                color: #3A1A5E;
                font-size: 14px;
                font-weight: bold;
                border-radius: 18px;
                padding: 8px 26px;
            }
            QPushButton:hover {
                background-color: #9E99AF;
            }
        """

    def _light_button(self) -> str:
        return """
            QPushButton {
                background-color: #EADDF8;
                color: #3A1A5E;
                font-size: 14px;
                font-weight: bold;
                border-radius: 18px;
                padding: 8px 26px;
            }
            QPushButton:hover {
                background-color: #DDC8F0;
            }
        """

    def _section_title(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet("""
            QLabel {
                font-size: 17px;
                font-weight: bold;
                color: #3A1A5E;
            }
        """)
        return label

    def _hr_line(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #3A1A5E; border: none;")
        return line

    def _sidebar_button(self, icon_path: str, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(24, 24))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 6px 10px;
                color: #4A2A6A;
                font-size: 15px;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #D9CFE6;
                border-radius: 6px;
            }
        """)
        return btn
