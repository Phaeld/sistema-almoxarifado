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
from auth.auth_service import AuthService
from material_service import MaterialService
from action_service import ActionService
from datetime import datetime


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
        self.ui.btn_sidebar_consultar.clicked.connect(self.show_consult_page)

        # Solicitar
        self.ui.btn_sidebar_solicitar.clicked.connect(self.show_request_page)

        # Cadastro de Funcionários
        self.ui.btn_sidebar_cad_func.clicked.connect(self.show_cad_func_page)

        # (Relatório / Imprimir / Exportar e Ajuda você liga depois, quando tiver as telas)

        # -----------------------------
        #  BOTÃO FILTRAR MATERIAIS
        # -----------------------------
        self.ui.btn_filter_materials.clicked.connect(self.apply_filters)

        # -----------------------------
        #  BOTÃO FILTRAR CONSULTAR
        # -----------------------------
        self.ui.btn_filter_consult.clicked.connect(self.apply_consult_filters)

        # -----------------------------
        #  AÇÕES DA TELA SOLICITAR (MODO CONSULTA)
        # -----------------------------
        self._request_mode = "new"
        self._current_action = None
        self.ui.btn_req_cancel.clicked.connect(
            lambda: self.handle_action_status("CANCELADO")
        )
        self.ui.btn_req_confirm.clicked.connect(
            lambda: self.handle_action_status("CONFIRMADO")
        )
        self.ui.btn_req_clear.clicked.connect(self.back_from_action_detail)

        # -----------------------------
        #  PRIMEIRA CARGA DA TABELA
        # -----------------------------
        self.load_materials()

        self.show()

        # Tabela consultar: selecionar linha inteira e abrir no duplo clique
        self.ui.table_consult.setSelectionBehavior(QTableWidget.SelectRows)
        self.ui.table_consult.setSelectionMode(QTableWidget.SingleSelection)
        self.ui.table_consult.cellDoubleClicked.connect(self.open_action_from_table)

        # Solicitar: preparar combos e eventos
        self._request_items = []
        self.setup_request_form()

        # Cadastro de funcionarios
        self.setup_employee_form()

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
    #  CARREGAR / FILTRAR AÇÕES (CONSULTAR)
    # ============================================================
    def show_consult_page(self):
        self.ui.pages_stack.setCurrentWidget(self.ui.page_consultar)
        self.load_actions()

    def load_actions(self):
        rows = ActionService.get_actions()
        self.populate_actions_table(rows)

    def apply_consult_filters(self):
        subject = self.ui.cons_input_subject.text().strip()
        id_action = self.ui.cons_input_action.text().strip()
        observation = self.ui.cons_input_obs.text().strip()
        date_str = self.ui.cons_input_date.text().strip()

        rows = ActionService.get_actions(
            subject=subject or None,
            id_action=id_action or None,
            observation=observation or None,
            date_str=date_str or None,
        )
        self.populate_actions_table(rows)

    def populate_actions_table(self, rows):
        table = self.ui.table_consult
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
    #  DETALHE DA AÇÃO (ABRIR NA TELA SOLICITAR)
    # ============================================================
    def show_request_page(self):
        self.ui.pages_stack.setCurrentWidget(self.ui.page_solicitar)
        self.set_request_mode("new")
        self.setup_request_form()

    def open_action_from_table(self, row, _column):
        item = self.ui.table_consult.item(row, 0)
        if not item:
            return

        id_action = item.text().strip()
        if not id_action:
            return

        data = ActionService.get_action_by_id(id_action)
        if not data:
            QMessageBox.warning(
                self,
                "Ação não encontrada",
                "Não foi possível carregar os dados da ação."
            )
            return

        self.fill_request_from_action(data)
        self.ui.pages_stack.setCurrentWidget(self.ui.page_solicitar)

    def fill_request_from_action(self, data):
        (
            id_action,
            matter,
            observation,
            category,
            solocitated,
            authorized,
            _date,
            id_item,
            descrption,
            quantity,
            status,
        ) = data

        self._current_action = {
            "id_action": id_action,
            "id_item": id_item,
            "quantity": quantity,
            "status": status,
        }

        self.set_request_mode("consult", id_action=id_action, status=status)

        # Categoria
        if category:
            if self.ui.req_combo_category.findText(category) == -1:
                self.ui.req_combo_category.addItem(category)
            self.ui.req_combo_category.setCurrentText(category)

        # Tipo (ACS/ACE)
        tipo = ""
        if id_action and id_action.startswith("ACS"):
            tipo = "SAÍDA"
        elif id_action and id_action.startswith("ACE"):
            tipo = "ENTRADA"
        if tipo:
            if self.ui.req_combo_type.findText(tipo) == -1:
                self.ui.req_combo_type.addItem(tipo)
            self.ui.req_combo_type.setCurrentText(tipo)

        # Descrição / Assunto
        self.ui.req_input_description.setText(str(matter or ""))

        # Itens
        self.ui.table_request_items.setRowCount(0)
        if id_item or descrption or quantity is not None:
            self.ui.table_request_items.setRowCount(1)
            self._set_table_item(self.ui.table_request_items, 0, 0, "✓")
            self._set_table_item(self.ui.table_request_items, 0, 1, id_item or "")
            self._set_table_item(self.ui.table_request_items, 0, 2, descrption or "")
            self._set_table_item(self.ui.table_request_items, 0, 3, quantity or "")

        # Solicitado por
        self.ui.req_input_requested_by.setText(str(solocitated or ""))

        # Observações
        self.ui.req_input_obs.setPlainText(str(observation or ""))

        # Autorizado por
        if authorized:
            if self.ui.req_combo_authorized.findText(authorized) == -1:
                self.ui.req_combo_authorized.addItem(authorized)
            self.ui.req_combo_authorized.setCurrentText(authorized)

    def set_request_mode(self, mode, id_action=None, status=None):
        self._request_mode = mode

        is_consult = mode == "consult"

        # Título
        if is_consult and id_action:
            self.ui.req_title.setText(f"TABELA - Solicitar (Ação {id_action})")
        else:
            self.ui.req_title.setText("TABELA - Solicitar")

        # Campos
        self.ui.req_combo_category.setEnabled(not is_consult)
        self.ui.req_combo_type.setEnabled(not is_consult)
        self.ui.req_input_description.setReadOnly(is_consult)
        self.ui.req_input_requested_by.setReadOnly(is_consult)
        self.ui.req_input_obs.setReadOnly(is_consult)
        self.ui.req_combo_authorized.setEnabled(not is_consult)

        if is_consult:
            self.ui.table_request_items.setEditTriggers(QTableWidget.NoEditTriggers)
        else:
            self.ui.table_request_items.setEditTriggers(
                QTableWidget.DoubleClicked | QTableWidget.SelectedClicked
            )

        # Botões
        if is_consult:
            self.ui.btn_req_clear.setText("VOLTAR")
            self.ui.btn_req_cancel.setText("CANCELADO")
            self.ui.btn_req_confirm.setText("CONFIRMADO")
            self.ui.btn_req_clear.show()
            self.ui.btn_req_cancel.show()
            self.ui.btn_req_confirm.show()
            level = self.user.get("level")
            if str(level) == "0" or level == 0:
                self.ui.btn_req_cancel.hide()
                self.ui.btn_req_confirm.hide()
            else:
                self.ui.btn_req_cancel.show()
                self.ui.btn_req_confirm.show()
                if status in ("CONFIRMADO", "CANCELADO"):
                    self.ui.btn_req_cancel.setEnabled(False)
                    self.ui.btn_req_confirm.setEnabled(False)
                else:
                    self.ui.btn_req_cancel.setEnabled(True)
                    self.ui.btn_req_confirm.setEnabled(True)
        else:
            self.ui.btn_req_cancel.setText("CANCELAR")
            self.ui.btn_req_clear.setText("LIMPAR")
            self.ui.btn_req_confirm.setText("CONFIRMAR")
            self.ui.btn_req_cancel.setEnabled(True)
            self.ui.btn_req_confirm.setEnabled(True)

    def handle_action_status(self, status):
        if self._request_mode != "consult":
            return

        if status == "CANCELADO":
            ActionService.update_action_status(
                self._current_action.get("id_action"), "CANCELADO"
            )
            QMessageBox.information(
                self,
                "Ação cancelada",
                "Ação marcada como CANCELADO."
            )
            self.show_consult_page()
            return

        if status == "CONFIRMADO":
            ok = self.apply_action_to_stock()
            if ok:
                ActionService.update_action_status(
                    self._current_action.get("id_action"), "CONFIRMADO"
                )
                QMessageBox.information(
                    self,
                    "Ação confirmada",
                    "Estoque atualizado e ação confirmada."
                )
                self.show_consult_page()
            return

        QMessageBox.information(
            self,
            "Status da Ação",
            f"Ação marcada como {status}."
        )
        self.show_consult_page()

    def back_from_action_detail(self):
        if self._request_mode != "consult":
            return
        self.show_consult_page()

    def _set_table_item(self, table, row, col, value):
        item = QTableWidgetItem(str(value))
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        table.setItem(row, col, item)

    # ============================================================
    #  SOLICITAR (NOVO)
    # ============================================================
    def setup_request_form(self):
        # Combos
        self.ui.req_combo_category.clear()
        self.ui.req_combo_category.addItems([
            "Selecione",
            "Limpeza, Higiene e Alimentos",
            "Elétrica",
            "Hidráulica",
            "Ferramentas Gerais",
            "Automóveis",
        ])

        self.ui.req_combo_type.clear()
        self.ui.req_combo_type.addItems(["Selecione", "Saída (ACS)", "Entrada (ACE)"])

        self.ui.req_combo_authorized.setEditable(True)

        try:
            self.ui.req_combo_category.currentTextChanged.disconnect()
        except TypeError:
            pass
        self.ui.req_combo_category.currentTextChanged.connect(self.load_request_items)

        try:
            self.ui.btn_req_confirm.clicked.disconnect()
        except TypeError:
            pass
        self.ui.btn_req_confirm.clicked.connect(self.submit_request)

        try:
            self.ui.btn_req_clear.clicked.disconnect()
        except TypeError:
            pass
        self.ui.btn_req_clear.clicked.connect(self.clear_request_form)

        self.load_request_items()

    def clear_request_form(self):
        self.ui.req_combo_category.setCurrentIndex(0)
        self.ui.req_combo_type.setCurrentIndex(0)
        self.ui.req_input_description.clear()
        self.ui.req_input_requested_by.clear()
        self.ui.req_input_obs.clear()
        self.ui.req_combo_authorized.setCurrentIndex(0)
        self.load_request_items()

    def load_request_items(self):
        category_text = self.ui.req_combo_category.currentText()
        tag_map = {
            "Limpeza, Higiene e Alimentos": "LIM",
            "Elétrica": "ELE",
            "Hidráulica": "HID",
            "Ferramentas Gerais": "FER",
            "Automóveis": "AUT",
        }
        tag = tag_map.get(category_text)

        if not tag:
            self.populate_request_items([])
            return

        rows = MaterialService.get_materials(
            category_tag=tag,
            description=None,
            item_number=None,
            product=None,
            category=None,
        )
        self.populate_request_items(rows)

    def populate_request_items(self, rows):
        table = self.ui.table_request_items
        table.setRowCount(0)
        self._request_items = rows

        if not rows:
            return

        table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            id_item, descr, _product, _category, _qty, _unit = row

            btn = QPushButton("+")
            btn.setFixedWidth(30)
            btn.clicked.connect(lambda _=None, r=row_index: self.toggle_request_item(r))
            table.setCellWidget(row_index, 0, btn)

            self._set_table_item(table, row_index, 1, id_item)
            self._set_table_item(table, row_index, 2, descr)

            spin = QSpinBox()
            spin.setRange(0, 9999)
            spin.setValue(0)
            table.setCellWidget(row_index, 3, spin)

    def toggle_request_item(self, row_index):
        table = self.ui.table_request_items
        btn = table.cellWidget(row_index, 0)
        if not btn:
            return
        if btn.text() == "+":
            btn.setText("-")
        else:
            btn.setText("+")
            spin = table.cellWidget(row_index, 3)
            if spin:
                spin.setValue(0)

    def submit_request(self):
        if self._request_mode != "new":
            # Em modo consulta, CONFIRMAR deve seguir o fluxo de confirmação
            self.handle_action_status("CONFIRMADO")
            return

        category = self.ui.req_combo_category.currentText()
        request_type = self.ui.req_combo_type.currentText()
        description = self.ui.req_input_description.text().strip()
        requested_by = self.ui.req_input_requested_by.text().strip()
        observation = self.ui.req_input_obs.toPlainText().strip()
        authorized = self.ui.req_combo_authorized.currentText().strip()

        if category == "Selecione":
            QMessageBox.warning(self, "Dados inválidos", "Selecione a categoria.")
            return
        if request_type == "Selecione":
            QMessageBox.warning(self, "Dados inválidos", "Selecione o tipo de solicitação.")
            return
        if not requested_by:
            QMessageBox.warning(self, "Dados inválidos", "Informe quem solicitou.")
            return

        prefix = "ACS" if "Saída" in request_type else "ACE"

        table = self.ui.table_request_items
        selected_rows = []
        for row_index in range(table.rowCount()):
            btn = table.cellWidget(row_index, 0)
            spin = table.cellWidget(row_index, 3)
            if btn and btn.text() == "-" and spin and spin.value() > 0:
                id_item = table.item(row_index, 1).text()
                descr = table.item(row_index, 2).text()
                qty = spin.value()
                selected_rows.append((id_item, descr, qty))

        if not selected_rows:
            QMessageBox.warning(self, "Itens", "Selecione ao menos um item e quantidade.")
            return

        date_str = datetime.now().strftime("%d/%m/%Y")
        for id_item, descr, qty in selected_rows:
            id_action = ActionService.get_next_action_id(prefix)
            ActionService.insert_action(
                id_action=id_action,
                matter=description,
                observation=observation,
                category=category,
                solocitated=requested_by,
                authorized=authorized,
                date_str=date_str,
                id_item=id_item,
                descrption=descr,
                quantity=qty,
            )

        QMessageBox.information(self, "Solicitação", "Movimento gerado com sucesso.")
        self.show_consult_page()

    def apply_action_to_stock(self):
        """
        Atualiza o estoque conforme o tipo da ação:
        ACE -> entrada (soma)
        ACS -> saída (subtrai)
        """
        if not self._current_action:
            QMessageBox.warning(
                self,
                "Ação inválida",
                "Não há ação carregada para atualizar o estoque."
            )
            return False

        id_item = (self._current_action.get("id_item") or "").strip()
        quantity = self._current_action.get("quantity")
        id_action = (self._current_action.get("id_action") or "").strip()

        if not id_item:
            QMessageBox.warning(
                self,
                "Item não informado",
                "A ação não possui número de item para atualizar o estoque."
            )
            return False

        if quantity is None:
            QMessageBox.warning(
                self,
                "Quantidade inválida",
                "A ação não possui quantidade informada."
            )
            return False

        try:
            qty_value = float(quantity)
        except (TypeError, ValueError):
            QMessageBox.warning(
                self,
                "Quantidade inválida",
                "A quantidade da ação não é numérica."
            )
            return False

        if qty_value <= 0:
            QMessageBox.warning(
                self,
                "Quantidade inválida",
                "A quantidade deve ser maior que zero."
            )
            return False

        # Define o delta conforme o tipo da ação
        if id_action.startswith("ACE"):
            delta = qty_value
        else:
            # padrão: ACS (saída)
            delta = -qty_value

        ok, message, _new_qty = MaterialService.update_material_quantity(
            id_item, delta
        )
        if not ok:
            QMessageBox.warning(self, "Falha ao atualizar", message)
            return False

        return True
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

    # ============================================================
    #  CADASTRO DE FUNCIONARIOS
    # ============================================================
    def show_cad_func_page(self):
        position = (self.user.get("position") or "").upper()
        if position not in {"ADMIN", "COORD"}:
            QMessageBox.warning(
                self,
                "Acesso negado",
                "Somente ADMIN ou COORD podem cadastrar usuarios."
            )
            return
        self.ui.pages_stack.setCurrentWidget(self.ui.page_cad_func)

    def setup_employee_form(self):
        self.ui.emp_combo_level.clear()
        self.ui.emp_combo_level.addItems(["Selecione", "0", "1"])

        self.ui.emp_combo_position.clear()
        self.ui.emp_combo_position.addItems([
            "Selecione",
            "ADMIN",
            "COORD",
            "ABAST",
            "COMUM",
        ])

        try:
            self.ui.btn_emp_register.clicked.disconnect()
        except TypeError:
            pass
        self.ui.btn_emp_register.clicked.connect(self.register_employee)

        try:
            self.ui.btn_emp_clear.clicked.disconnect()
        except TypeError:
            pass
        self.ui.btn_emp_clear.clicked.connect(self.clear_employee_form)

        try:
            self.ui.btn_emp_cancel.clicked.disconnect()
        except TypeError:
            pass
        self.ui.btn_emp_cancel.clicked.connect(self.show_consult_page)

    def clear_employee_form(self):
        self.ui.emp_input_username.clear()
        self.ui.emp_input_fullname.clear()
        self.ui.emp_combo_level.setCurrentIndex(0)
        self.ui.emp_combo_position.setCurrentIndex(0)
        self.ui.emp_input_session.clear()
        self.ui.emp_input_password.clear()
        self.ui.emp_input_confirm.clear()

    def register_employee(self):
        position = (self.user.get("position") or "").upper()
        if position not in {"ADMIN", "COORD"}:
            QMessageBox.warning(
                self,
                "Acesso negado",
                "Somente ADMIN ou COORD podem cadastrar usuarios."
            )
            return

        username = self.ui.emp_input_username.text().strip()
        fullname = self.ui.emp_input_fullname.text().strip()
        level_text = self.ui.emp_combo_level.currentText().strip()
        position_text = self.ui.emp_combo_position.currentText().strip()
        tag = self.ui.emp_input_session.text().strip()
        password = self.ui.emp_input_password.text()
        confirm = self.ui.emp_input_confirm.text()

        if not username:
            QMessageBox.warning(self, "Dados invalidos", "Informe o usuario.")
            return
        if not fullname:
            QMessageBox.warning(self, "Dados invalidos", "Informe o nome completo.")
            return
        if level_text == "Selecione":
            QMessageBox.warning(self, "Dados invalidos", "Selecione o nivel.")
            return
        if position_text == "Selecione":
            QMessageBox.warning(self, "Dados invalidos", "Selecione o cargo.")
            return
        if not tag:
            QMessageBox.warning(self, "Dados invalidos", "Informe a sessao/tag.")
            return
        if not password:
            QMessageBox.warning(self, "Dados invalidos", "Informe a senha.")
            return
        if password != confirm:
            QMessageBox.warning(self, "Dados invalidos", "As senhas nao conferem.")
            return

        if AuthService.username_exists(username):
            QMessageBox.warning(self, "Dados invalidos", "Usuario ja existe.")
            return

        try:
            level_value = int(level_text)
        except ValueError:
            QMessageBox.warning(self, "Dados invalidos", "Nivel invalido.")
            return

        AuthService.create_user(
            username=username,
            name=fullname,
            password=password,
            position=position_text,
            level=level_value,
            tag=tag,
        )
        QMessageBox.information(self, "Cadastro", "Usuario cadastrado com sucesso.")
        self.clear_employee_form()
