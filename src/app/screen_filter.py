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
import json

from qt_core import *

from gui.window.main_window.ui_screen_filter_window import UI_ScreenFilterWindow
from auth.session import Session
from auth.auth_service import AuthService
from material_service import MaterialService
from action_service import ActionService
from log_service import LogService
from datetime import datetime, timedelta
import io
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QTextDocument
from pathlib import Path


class ScreenFilterWindow(QMainWindow):
    def __init__(self, category_tag: str):
        super().__init__()

        # -----------------------------
        #  SessÃ£o
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

        # PÃ¡gina inicial sempre a de materiais
        self.ui.pages_stack.setCurrentWidget(self.ui.page_materials)

        # -----------------------------
        #  ConexÃµes TOP BAR
        # -----------------------------
        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)

        # -----------------------------
        #  ConexÃµes SIDEBAR â€“ CATEGORIA
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
        #  ConexÃµes SIDEBAR â€“ AÃ‡Ã•ES
        # -----------------------------
        # Consultar
        self.ui.btn_sidebar_consultar.clicked.connect(self.show_consult_page)

        # Solicitar
        self.ui.btn_sidebar_solicitar.clicked.connect(self.show_request_page)

        # Cadastro de FuncionÃ¡rios
        self.ui.btn_sidebar_cad_func.clicked.connect(self.show_cad_func_page)

        # Relatorio
        self.ui.btn_sidebar_relatorio.clicked.connect(self.show_report_page)
        self.ui.btn_sidebar_exportar.clicked.connect(self.export_stock_report_pdf)
        self.ui.btn_sidebar_imprimir.clicked.connect(self.print_stock_report)
        self.ui.btn_sidebar_ajuda.clicked.connect(self.open_help)

        # (RelatÃ³rio / Imprimir / Exportar e Ajuda vocÃª liga depois, quando tiver as telas)

        # -----------------------------
        #  BOTÃƒO FILTRAR MATERIAIS
        # -----------------------------
        self.ui.btn_filter_materials.clicked.connect(self.apply_filters)

        # -----------------------------
        #  BOTÃƒO FILTRAR CONSULTAR
        # -----------------------------
        self.ui.btn_filter_consult.clicked.connect(self.apply_consult_filters)

        # -----------------------------
        #  AÃ‡Ã•ES DA TELA SOLICITAR (MODO CONSULTA)
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
        self._custom_request_items = []
        self.setup_request_form()

        # Cadastro de funcionarios
        self.setup_employee_form()

        # Relatorio
        self.setup_report_form()

    # ============================================================
    #  CARREGAR / FILTRAR MATERIAIS
    # ============================================================
    def change_category(self, tag: str):
        """
        Chamado quando o usuÃ¡rio clica numa categoria do sidebar.
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
        BotÃ£o FILTRAR da pÃ¡gina de materiais.
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
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # sÃ³ leitura
                table.setItem(row_index, col_index, item)

    # ============================================================
    #  CARREGAR / FILTRAR AÃ‡Ã•ES (CONSULTAR)
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
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # sÃ³ leitura
                table.setItem(row_index, col_index, item)

    # ============================================================
    #  DETALHE DA AÃ‡ÃƒO (ABRIR NA TELA SOLICITAR)
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
                "AÃ§Ã£o nÃ£o encontrada",
                "NÃ£o foi possÃ­vel carregar os dados da aÃ§Ã£o."
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
            tipo = "Saida (ACS)"
        elif id_action and id_action.startswith("ACE"):
            tipo = "Entrada (ACE)"
        if tipo:
            if self.ui.req_combo_type.findText(tipo) == -1:
                self.ui.req_combo_type.addItem(tipo)
            self.ui.req_combo_type.setCurrentText(tipo)

        # DescriÃ§Ã£o / Assunto
        self.ui.req_input_description.setText(str(matter or ""))

        # Itens
        self.ui.table_request_items.setRowCount(0)
        parsed_items = self._parse_action_items(id_item, descrption, quantity)
        if parsed_items:
            self.ui.table_request_items.setRowCount(len(parsed_items))
            for row_index, item_data in enumerate(parsed_items):
                self._set_table_item(self.ui.table_request_items, row_index, 0, "✓")
                item_number = item_data["id_item"]
                display_item = item_number
                if item_number.startswith("NEWJSON:"):
                    try:
                        payload = json.loads(item_number[len("NEWJSON:"):])
                        display_item = payload.get("id_item_preview") or "NOVO"
                    except json.JSONDecodeError:
                        display_item = "NOVO"
                item_cell = QTableWidgetItem(str(display_item))
                item_cell.setFlags(item_cell.flags() ^ Qt.ItemIsEditable)
                item_cell.setData(Qt.UserRole, item_number)
                self.ui.table_request_items.setItem(row_index, 1, item_cell)
                self._set_table_item(self.ui.table_request_items, row_index, 2, item_data["descr"])
                self._set_table_item(self.ui.table_request_items, row_index, 3, item_data["qty"])

        # Solicitado por
        self.ui.req_input_requested_by.setText(str(solocitated or ""))

        # ObservaÃ§Ãµes
        self.ui.req_input_obs.setPlainText(str(observation or ""))

        # Autorizado por
        if authorized:
            if self.ui.req_combo_authorized.findText(authorized) == -1:
                self.ui.req_combo_authorized.addItem(authorized)
            self.ui.req_combo_authorized.setCurrentText(authorized)

    def set_request_mode(self, mode, id_action=None, status=None):
        self._request_mode = mode

        is_consult = mode == "consult"

        # Titulo
        if is_consult and id_action:
            self.ui.req_title.setText(f"TABELA - Solicitar (Acao {id_action})")
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

        # BotÃµes
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
            LogService.log_event(
                "ACTION_CANCELLED",
                f"id_action={self._current_action.get('id_action')} id_item={self._current_action.get('id_item')} qty={self._current_action.get('quantity')}",
                self.user,
            )
            QMessageBox.information(
                self,
                "AÃ§Ã£o cancelada",
                "AÃ§Ã£o marcada como CANCELADO."
            )
            self.show_consult_page()
            return

        if status == "CONFIRMADO":
            ok = self.apply_action_to_stock()
            if ok:
                ActionService.update_action_status(
                    self._current_action.get("id_action"), "CONFIRMADO"
                )
                LogService.log_event(
                    "ACTION_CONFIRMED",
                    f"id_action={self._current_action.get('id_action')} id_item={self._current_action.get('id_item')} qty={self._current_action.get('quantity')}",
                    self.user,
                )
                QMessageBox.information(
                    self,
                    "AÃ§Ã£o confirmada",
                    "Estoque atualizado e aÃ§Ã£o confirmada."
                )
                self.show_consult_page()
            return

        QMessageBox.information(
            self,
            "Status da AÃ§Ã£o",
            f"AÃ§Ã£o marcada como {status}."
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
            "Eletrica",
            "Hidraulica",
            "Ferramentas Gerais",
            "Automoveis",
        ])

        self.ui.req_combo_type.clear()
        self.ui.req_combo_type.addItems(["Selecione", "Saida (ACS)", "Entrada (ACE)"])

        self.ui.req_combo_authorized.clear()
        self.ui.req_combo_authorized.setEditable(False)
        self.ui.req_combo_authorized.addItems([
            "Selecione",
            "Aide Rodrigues de Novaes Bigi",
            "Luiza Eduardo da Silva",
            "Raphael da Silva",
        ])

        try:
            self.ui.req_combo_category.currentTextChanged.disconnect()
        except TypeError:
            pass
        self.ui.req_combo_category.currentTextChanged.connect(self.load_request_items)

        try:
            self.ui.req_input_item_search.textChanged.disconnect()
        except TypeError:
            pass
        self.ui.req_input_item_search.textChanged.connect(self.load_request_items)

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

        try:
            self.ui.btn_add_material.clicked.disconnect()
        except TypeError:
            pass
        self.ui.btn_add_material.clicked.connect(self.open_add_material_dialog)

        self.load_request_items()

    def clear_request_form(self):
        self.ui.req_combo_category.setCurrentIndex(0)
        self.ui.req_combo_type.setCurrentIndex(0)
        self.ui.req_input_description.clear()
        self.ui.req_input_requested_by.clear()
        self.ui.req_input_obs.clear()
        self.ui.req_combo_authorized.setCurrentIndex(0)
        self.ui.req_input_item_search.clear()
        self._custom_request_items = []
        self.load_request_items()

    def load_request_items(self):
        category_text = self.ui.req_combo_category.currentText()
        search_text = self.ui.req_input_item_search.text().strip().lower()
        tag_map = {
            "Limpeza, Higiene e Alimentos": "LIM",
            "Eletrica": "ELE",
            "Hidraulica": "HID",
            "Ferramentas Gerais": "FER",
            "Automoveis": "AUT",
            "Eletrica": "ELE",
            "Hidraulica": "HID",
            "Automoveis": "AUT",
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
        if search_text:
            rows = [r for r in rows if search_text in str(r[1] or "").lower()]

        custom_rows = []
        for item_data in self._custom_request_items:
            if item_data["category"] != category_text:
                continue
            if search_text and search_text not in item_data["descr"].lower():
                continue
            token = self._build_new_item_token(item_data)
            custom_rows.append(
                (
                    item_data.get("id_item_preview", ""),
                    item_data["descr"],
                    item_data["product"],
                    item_data["category"],
                    float(item_data["qty"]),
                    item_data["unit"],
                    token,
                )
            )

        rows = list(rows) + custom_rows
        self.populate_request_items(rows)

    def populate_request_items(self, rows):
        table = self.ui.table_request_items
        table.setRowCount(0)
        self._request_items = rows

        if not rows:
            return

        table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            if len(row) >= 7:
                id_item, descr, _product, _category, _qty, _unit, internal_id = row
            else:
                id_item, descr, _product, _category, _qty, _unit = row
                internal_id = id_item

            btn = QPushButton("+")
            btn.setFixedWidth(30)
            btn.clicked.connect(lambda _=None, r=row_index: self.toggle_request_item(r))
            table.setCellWidget(row_index, 0, btn)

            self._set_table_item(table, row_index, 1, id_item)
            item_cell = table.item(row_index, 1)
            if item_cell:
                item_cell.setData(Qt.UserRole, internal_id)
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
            self.handle_action_status("CONFIRMADO")
            return

        category = self.ui.req_combo_category.currentText()
        request_type = self.ui.req_combo_type.currentText()
        description = self.ui.req_input_description.text().strip()
        requested_by = self.ui.req_input_requested_by.text().strip()
        observation = self.ui.req_input_obs.toPlainText().strip()
        authorized = self.ui.req_combo_authorized.currentText().strip()

        if category == "Selecione":
            QMessageBox.warning(self, "Dados invalidos", "Selecione a categoria.")
            return
        if request_type == "Selecione":
            QMessageBox.warning(self, "Dados invalidos", "Selecione o tipo de solicitacao.")
            return
        if not requested_by:
            QMessageBox.warning(self, "Dados invalidos", "Informe quem solicitou.")
            return
        if authorized == "Selecione":
            QMessageBox.warning(self, "Dados invalidos", "Selecione quem autorizou.")
            return

        prefix = "ACS" if ("Saida" in request_type or "Saída" in request_type) else "ACE"

        table = self.ui.table_request_items
        selected_rows = []
        for row_index in range(table.rowCount()):
            btn = table.cellWidget(row_index, 0)
            spin = table.cellWidget(row_index, 3)
            if btn and btn.text() == "-" and spin and spin.value() > 0:
                id_item_cell = table.item(row_index, 1)
                if not id_item_cell:
                    continue
                id_item = id_item_cell.data(Qt.UserRole) or id_item_cell.text()
                descr_cell = table.item(row_index, 2)
                descr = descr_cell.text() if descr_cell else ""
                qty = spin.value()
                selected_rows.append((id_item, descr, qty))

        if not selected_rows:
            QMessageBox.warning(self, "Itens", "Selecione ao menos um item e quantidade.")
            return

        date_str = datetime.now().strftime("%d/%m/%Y")
        id_action = ActionService.get_next_action_id(prefix)
        id_items = ";;".join(str(row[0]) for row in selected_rows)
        descrs = ";;".join(str(row[1]) for row in selected_rows)
        quantities = ";;".join(str(int(row[2])) for row in selected_rows)
        ActionService.insert_action(
            id_action=id_action,
            matter=description,
            observation=observation,
            category=category,
            solocitated=requested_by,
            authorized=authorized,
            date_str=date_str,
            id_item=id_items,
            descrption=descrs,
            quantity=quantities,
        )
        LogService.log_event(
            "ACTION_CREATED",
            f"id_action={id_action} items={len(selected_rows)} type={prefix}",
            self.user,
        )

        QMessageBox.information(self, "Solicitacao", "Movimento gerado com sucesso.")
        self.show_consult_page()

    def open_add_material_dialog(self):
        dialog = AddMaterialDialog(self)
        if dialog.exec() == QDialog.Accepted:
            item_data = getattr(dialog, "item_data", None)
            if item_data:
                self._custom_request_items.append(item_data)
            self.load_request_items()

    def apply_action_to_stock(self):
        """
        Atualiza o estoque conforme o tipo da acao:
        ACE -> entrada (soma)
        ACS -> saida (subtrai)
        """
        if not self._current_action:
            QMessageBox.warning(
                self,
                "Acao invalida",
                "Nao ha acao carregada para atualizar o estoque."
            )
            return False

        id_action = (self._current_action.get("id_action") or "").strip()

        table = self.ui.table_request_items
        if table.rowCount() == 0:
            QMessageBox.warning(self, "Sem itens", "A acao nao possui itens.")
            return False

        for row_index in range(table.rowCount()):
            item_cell = table.item(row_index, 1)
            qty_cell = table.item(row_index, 3)
            descr_cell = table.item(row_index, 2)
            if not item_cell or not qty_cell:
                continue

            id_item = (item_cell.data(Qt.UserRole) or item_cell.text() or "").strip()
            descr = (descr_cell.text() if descr_cell else "").strip()
            try:
                qty_value = float(str(qty_cell.text()).replace(",", "."))
            except (TypeError, ValueError):
                QMessageBox.warning(self, "Quantidade invalida", "Item com quantidade invalida.")
                return False

            if qty_value <= 0:
                continue

            if id_item.startswith("NEWJSON:"):
                if not id_action.startswith("ACE"):
                    QMessageBox.warning(
                        self,
                        "Item novo invalido",
                        "Item novo so pode ser confirmado em solicitacao de entrada (ACE).",
                    )
                    return False
                try:
                    payload = json.loads(id_item[len("NEWJSON:"):])
                except json.JSONDecodeError:
                    QMessageBox.warning(self, "Dados invalidos", "Nao foi possivel ler o item novo.")
                    return False

                prefix_map = {
                    "Limpeza, Higiene e Alimentos": "L",
                    "Eletrica": "E",
                    "Hidraulica": "H",
                    "Ferramentas Gerais": "F",
                    "Automoveis": "A",
                    "Elétrica": "E",
                    "Hidráulica": "H",
                    "Automóveis": "A",
                }
                prefix = prefix_map.get(payload.get("category"))
                if not prefix:
                    QMessageBox.warning(self, "Categoria invalida", "Categoria do item novo invalida.")
                    return False

                new_id = MaterialService.get_next_item_id(prefix)
                MaterialService.create_material(
                    id_item=new_id,
                    descrption=payload.get("descr") or descr or "Sem descricao",
                    product=payload.get("product") or "N/A",
                    category=payload.get("category") or "",
                    quantity=qty_value,
                    unit_measurement=payload.get("unit") or "",
                )
                LogService.log_event(
                    "MATERIAL_CREATE_FROM_ACE",
                    f"id_action={id_action} id_item={new_id} qty={qty_value}",
                    self.user,
                )
                continue

            delta = qty_value if id_action.startswith("ACE") else -qty_value
            ok, message, _new_qty = MaterialService.update_material_quantity(id_item, delta)
            if not ok:
                QMessageBox.warning(self, "Falha ao atualizar", message)
                return False

        return True

    def _build_new_item_token(self, item_data):
        return "NEWJSON:" + json.dumps(item_data, ensure_ascii=True)

    def _parse_action_items(self, id_item_field, descr_field, quantity_field):
        ids = str(id_item_field or "").split(";;") if id_item_field else []
        descrs = str(descr_field or "").split(";;") if descr_field else []
        qtys = str(quantity_field or "").split(";;") if quantity_field else []
        size = max(len(ids), len(descrs), len(qtys), 0)
        items = []
        for i in range(size):
            items.append(
                {
                    "id_item": ids[i].strip() if i < len(ids) else "",
                    "descr": descrs[i].strip() if i < len(descrs) else "",
                    "qty": qtys[i].strip() if i < len(qtys) else "0",
                }
            )
        return items

    def _safe_float(self, value):
        try:
            return float(str(value).replace(",", "."))
        except (TypeError, ValueError):
            return 0.0

    # ============================================================
    #  NAVEGAÃ‡ÃƒO
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

    def open_help(self):
        from help import HelpWindow
        self.help = HelpWindow()
        self.help.show()
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

        try:
            self.ui.btn_emp_list.clicked.disconnect()
        except TypeError:
            pass
        self.ui.btn_emp_list.clicked.connect(self.open_employee_list)

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
        LogService.log_event(
            "USER_CREATE",
            f"username={username} position={position_text} level={level_value} tag={tag}",
            self.user,
        )
        LogService.log_event(
            "USER_CREATE",
            f"username={username} position={position_text} level={level_value} tag={tag}",
            self.user,
        )
        QMessageBox.information(self, "Cadastro", "Usuario cadastrado com sucesso.")
        self.clear_employee_form()

    # ============================================================
    #  RELATORIO (DASHBOARD)
    # ============================================================
    def show_report_page(self):
        self.ui.pages_stack.setCurrentWidget(self.ui.page_relatorio)
        self.update_report()

    def setup_report_form(self):
        # Meses
        self.ui.report_combo_month.clear()
        self.ui.report_combo_month.addItems([
            "Todos",
            "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ])

        # Categoria
        self.ui.report_combo_category.clear()
        self.ui.report_combo_category.addItems([
            "Todos",
            "Limpeza, Higiene e Alimentos",
            "Eletrica",
            "Hidraulica",
            "Ferramentas Gerais",
            "Automoveis",
        ])

        # Tipo
        self.ui.report_combo_type.clear()
        self.ui.report_combo_type.addItems(["Retirada", "Chegada"])

        # Periodo
        self.ui.report_combo_period.clear()
        self.ui.report_combo_period.addItems([
            "Diario", "Semanal", "Mensal", "Trimestral", "Semestral"
        ])

        self.ui.report_combo_month.currentTextChanged.connect(self.update_report)
        self.ui.report_combo_category.currentTextChanged.connect(self.update_report)
        self.ui.report_combo_type.currentTextChanged.connect(self.update_report)
        self.ui.report_combo_period.currentTextChanged.connect(self.update_report)

    def update_report(self):
        actions = self.load_actions_report()
        materials = self.load_materials_report()

        total_items = sum([float(r[4]) for r in materials]) if materials else 0
        self.ui.lbl_total_items.setText(str(int(total_items)))

        items_out = sum(self._safe_float(a[5]) for a in actions if a[0].startswith("ACS"))
        items_in = sum(self._safe_float(a[5]) for a in actions if a[0].startswith("ACE"))
        self.ui.lbl_items_out.setText(str(int(items_out)))
        self.ui.lbl_items_in.setText(str(int(items_in)))

        report_type = self.ui.report_combo_type.currentText()
        if report_type == "Chegada":
            self.ui.report_chart_title.setText("QNT. ITENS CHEGARAM NA SEMANA")
            self.ui.report_top_title.setText("ITENS MAIS CHEGARAM")
            item = max(materials, key=lambda r: r[4], default=None)
            self.ui.lbl_stock_item.setText(item[1] if item else "-")
            self.ui.lbl_stock_item.setToolTip(item[1] if item else "")
        else:
            self.ui.report_chart_title.setText("QNT. ITENS RETIRADOS NA SEMANA")
            self.ui.report_top_title.setText("ITENS MAIS SÃƒO RETIRADOS")
            item = min(materials, key=lambda r: r[4], default=None)
            self.ui.lbl_stock_item.setText(item[1] if item else "-")
            self.ui.lbl_stock_item.setToolTip(item[1] if item else "")

        self.update_top_items(actions)
        self.update_chart(actions)

    def load_actions_report(self):
        rows = ActionService.list_actions()
        data = []
        for r in rows:
            parsed_items = self._parse_action_items(r[7], r[8], r[9])
            if parsed_items:
                for item in parsed_items:
                    data.append(
                        (
                            r[0],
                            r[3],
                            r[6],
                            item["id_item"],
                            item["descr"],
                            self._safe_float(item["qty"]),
                        )
                    )
            else:
                data.append((r[0], r[3], r[6], r[7], r[8], self._safe_float(r[9])))

        # filtros
        category = self.ui.report_combo_category.currentText()
        if category != "Todos":
            data = [r for r in data if category.lower() in (r[1] or "").lower()]

        month = self.ui.report_combo_month.currentText()
        if month != "Todos":
            month_map = {
                "Janeiro": 1, "Fevereiro": 2, "Marco": 3, "Abril": 4, "Maio": 5, "Junho": 6,
                "Julho": 7, "Agosto": 8, "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
            }
            target = month_map.get(month)
            if target:
                data = [r for r in data if self._date_month(r[2]) == target]

        return data

    def load_materials_report(self):
        category = self.ui.report_combo_category.currentText()
        tag_map = {
            "Limpeza, Higiene e Alimentos": "LIM",
            "Eletrica": "ELE",
            "Hidraulica": "HID",
            "Ferramentas Gerais": "FER",
            "Automoveis": "AUT",
        }
        tag = tag_map.get(category) if category != "Todos" else None

        rows = MaterialService.get_materials(
            category_tag=tag,
            description=None,
            item_number=None,
            product=None,
            category=None,
        )
        return rows

    def update_top_items(self, actions):
        report_type = self.ui.report_combo_type.currentText()
        prefix = "ACE" if report_type == "Chegada" else "ACS"
        items = {}
        for id_action, _category, _date, _id_item, descr, qty in actions:
            if not id_action.startswith(prefix):
                continue
            items[descr] = items.get(descr, 0) + (qty or 0)

        top = sorted(items.items(), key=lambda x: x[1], reverse=True)[:5]

        table = self.ui.report_top_items
        table.setRowCount(0)
        if not top:
            return
        table.setRowCount(len(top))
        for i, (descr, _qty) in enumerate(top):
            text = descr if len(descr) <= 18 else descr[:18] + "..."
            item = QTableWidgetItem(text)
            item.setToolTip(descr)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            table.setItem(i, 0, item)

    def update_chart(self, actions):
        report_type = self.ui.report_combo_type.currentText()
        prefix = "ACE" if report_type == "Chegada" else "ACS"
        period = self.ui.report_combo_period.currentText()

        # window length
        days_map = {
            "Diario": 1,
            "Semanal": 7,
            "Mensal": 30,
            "Trimestral": 90,
            "Semestral": 180,
        }
        days = days_map.get(period, 7)
        end = datetime.now()
        start = end - timedelta(days=days)

        buckets = {}
        for id_action, _category, date_str, _id_item, _descr, qty in actions:
            if not id_action.startswith(prefix):
                continue
            dt = self._parse_date(date_str)
            if not dt:
                continue
            if dt < start or dt > end:
                continue
            key = dt.strftime("%d/%m")
            buckets[key] = buckets.get(key, 0) + (qty or 0)

        labels = list(buckets.keys())
        values = [buckets[k] for k in labels]

        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            self.ui.report_chart.setText("Instale matplotlib para exibir o grÃ¡fico.")
            return

        fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
        ax.bar(labels, values, color="#9B3D97")
        ax.set_ylabel("Quantidade")
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.ui.report_chart.setPixmap(pixmap)
        self.ui.report_chart.setText("")

    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except (TypeError, ValueError):
            return None

    def _date_month(self, date_str):
        dt = self._parse_date(date_str)
        return dt.month if dt else None

    # ============================================================
    #  IMPRESSÃƒO â€“ RELATÃ“RIO COMPLETO DE ESTOQUE
    # ============================================================
    def print_stock_report(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec() != QDialog.Accepted:
            return

        html = self.build_stock_report_html()
        doc = QTextDocument()
        doc.setHtml(html)
        doc.print_(printer)

    def export_stock_report_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exportar PDF", "", "PDF (*.pdf)"
        )
        if not file_path:
            return

        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_path)

        html = self.build_stock_report_html()
        doc = QTextDocument()
        doc.setHtml(html)
        doc.print_(printer)

        QMessageBox.information(self, "Exportar", "PDF gerado com sucesso.")

    def build_stock_report_html(self):
        # Dados
        materials = MaterialService.get_materials(
            category_tag=None,
            description=None,
            item_number=None,
            product=None,
            category=None,
        )
        actions = ActionService.list_actions()

        # Totais
        total_stock = sum(float(r[4]) for r in materials) if materials else 0
        total_out = sum((a[9] or 0) for a in actions if a[0].startswith("ACS"))
        total_in = sum((a[9] or 0) for a in actions if a[0].startswith("ACE"))

        # Itens mais pegos (saÃ­das)
        picked = {}
        for a in actions:
            if not a[0].startswith("ACS"):
                continue
            descr = a[8]
            qty = a[9] or 0
            picked[descr] = picked.get(descr, 0) + qty
        top_picked = sorted(picked.items(), key=lambda x: x[1], reverse=True)[:10]

        # Logo
        logo_path = (Path(__file__).resolve().parents[2] / "assets" / "logo_secretaria.png")
        logo_uri = logo_path.as_uri()

        def row_material(m):
            qty = float(m[4])
            color = "color:#B00020; font-weight:bold;" if qty < 10 else ""
            return f"""
                <tr>
                    <td>{m[0]}</td>
                    <td>{m[1]}</td>
                    <td>{m[2]}</td>
                    <td>{m[3]}</td>
                    <td style="{color}">{qty}</td>
                    <td>{m[5]}</td>
                </tr>
            """

        def row_action(a):
            return f"""
                <tr>
                    <td>{a[0]}</td>
                    <td>{a[3]}</td>
                    <td>{a[6]}</td>
                    <td>{a[7]}</td>
                    <td>{a[8]}</td>
                    <td>{a[9]}</td>
                    <td>{a[10] or ""}</td>
                </tr>
            """

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #3A1A5E; font-size: 14px; }}
                h1 {{ color: #3E0F63; font-size: 24px; }}
                h2 {{ color: #3E0F63; font-size: 18px; margin-top: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th, td {{ border: 1px solid #CBB2E6; padding: 8px; font-size: 14px; }}
                th {{ background: #E6D9F2; color: #3E0F63; }}
                .kpi {{ margin: 8px 0; font-size: 15px; }}
            </style>
        </head>
        <body>
            <div style="display:flex; align-items:center; gap:12px;">
                <img src="{logo_uri}" width="120"/>
                <div>
                    <h1>RelatÃ³rio Completo de Estoque</h1>
                    <div>{datetime.now().strftime("%d/%m/%Y %H:%M")}</div>
                </div>
            </div>

            <div class="kpi"><b>QNT. TOTAL DE ITENS:</b> {int(total_stock)}</div>
            <div class="kpi"><b>QNT. ITENS SAIU:</b> {int(total_out)}</div>
            <div class="kpi"><b>QNT. ITENS CHEGOU:</b> {int(total_in)}</div>

            <h2>Estoque Atual (itens com quantidade abaixo de 10 em vermelho)</h2>
            <table>
                <tr>
                    <th>NÃºmero</th><th>DescriÃ§Ã£o</th><th>Produto</th>
                    <th>Categoria</th><th>Quantidade</th><th>Un.</th>
                </tr>
                {''.join(row_material(m) for m in materials)}
            </table>

            <h2>AÃ§Ãµes (Entradas e Saidas)</h2>
            <table>
                <tr>
                    <th>ID AÃ§Ã£o</th><th>Categoria</th><th>Data</th>
                    <th>ID Item</th><th>DescriÃ§Ã£o</th><th>Quantidade</th><th>Status</th>
                </tr>
                {''.join(row_action(a) for a in actions)}
            </table>

            <h2>Itens Mais Pegos (Saidas)</h2>
            <table>
                <tr><th>DescriÃ§Ã£o</th><th>Quantidade</th></tr>
                {''.join(f"<tr><td>{d}</td><td>{q}</td></tr>" for d,q in top_picked)}
            </table>
        </body>
        </html>
        """
        return html

    def open_employee_list(self):
        dialog = EmployeeListDialog(self, self.user)
        dialog.exec()


class EmployeeListDialog(QDialog):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.setWindowTitle("Colaboradores")
        self.setMinimumSize(720, 420)
        self.setStyleSheet("background-color: #E8E2EE;")

        self.current_user = current_user
        self.is_admin_level1 = (
            (current_user.get("position") or "").upper() == "ADMIN"
            and str(current_user.get("level")) == "1"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "UsuÃ¡rio", "Nome", "Cargo", "NÃ­vel", "Tag"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #F8F3FF;
                gridline-color: #CBB2E6;
                color: #3A1A5E;
            }
            QHeaderView::section {
                background-color: #3E0F63;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border: none;
                padding: 6px;
            }
        """)
        layout.addWidget(self.table)

        form = QGridLayout()
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(8)

        label_style = "font-size: 12px; font-weight: bold; color: #3A1A5E;"
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

        self.input_username = QLineEdit()
        self.input_username.setStyleSheet(line_style)
        self.input_name = QLineEdit()
        self.input_name.setStyleSheet(line_style)
        self.input_password = QLineEdit()
        self.input_password.setStyleSheet(line_style)
        self.input_password.setEchoMode(QLineEdit.Password)

        self.combo_position = QComboBox()
        self.combo_position.setStyleSheet(combo_style)
        self.combo_position.addItems(["ADMIN", "COORD", "ABAST", "COMUM"])
        self.combo_level = QComboBox()
        self.combo_level.setStyleSheet(combo_style)
        self.combo_level.addItems(["0", "1"])
        self.input_tag = QLineEdit()
        self.input_tag.setStyleSheet(line_style)

        form.addWidget(QLabel("UsuÃ¡rio"), 0, 0)
        form.itemAt(0).widget().setStyleSheet(label_style)
        form.addWidget(self.input_username, 1, 0)
        form.addWidget(QLabel("Nome"), 0, 1)
        form.itemAt(2).widget().setStyleSheet(label_style)
        form.addWidget(self.input_name, 1, 1)
        form.addWidget(QLabel("Senha"), 0, 2)
        form.itemAt(4).widget().setStyleSheet(label_style)
        form.addWidget(self.input_password, 1, 2)
        form.addWidget(QLabel("Cargo"), 2, 0)
        form.itemAt(6).widget().setStyleSheet(label_style)
        form.addWidget(self.combo_position, 3, 0)
        form.addWidget(QLabel("NÃ­vel"), 2, 1)
        form.itemAt(8).widget().setStyleSheet(label_style)
        form.addWidget(self.combo_level, 3, 1)
        form.addWidget(QLabel("Tag"), 2, 2)
        form.itemAt(10).widget().setStyleSheet(label_style)
        form.addWidget(self.input_tag, 3, 2)

        layout.addLayout(form)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.btn_close = QPushButton("FECHAR")
        self.btn_close.setStyleSheet(self._light_button())
        self.btn_save = QPushButton("SALVAR")
        self.btn_save.setStyleSheet(self._primary_button())
        self.btn_delete = QPushButton("EXCLUIR")
        self.btn_delete.setStyleSheet(self._secondary_button())
        btn_row.addWidget(self.btn_close)
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_delete)
        layout.addLayout(btn_row)

        self.btn_close.clicked.connect(self.accept)
        self.btn_save.clicked.connect(self.save_user)
        self.btn_delete.clicked.connect(self.delete_user)

        if not self.is_admin_level1:
            self.input_username.setReadOnly(True)
            self.input_name.setReadOnly(True)
            self.input_password.setReadOnly(True)
            self.combo_position.setEnabled(False)
            self.combo_level.setEnabled(False)
            self.input_tag.setReadOnly(True)
            self.btn_save.setEnabled(False)
            self.btn_delete.setEnabled(False)

        self.table.itemSelectionChanged.connect(self.on_select_row)
        self.load_users()

    def load_users(self):
        rows = AuthService.list_users()
        self.table.setRowCount(0)
        self._rows = rows
        if not rows:
            return
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            for j, val in enumerate(r):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(i, j, item)

    def on_select_row(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self._rows):
            return
        user_id, username, name, position, level, tag = self._rows[row]
        self._selected_id = user_id
        self.input_username.setText(username)
        self.input_name.setText(name)
        self.combo_position.setCurrentText(position)
        self.combo_level.setCurrentText(str(level))
        self.input_tag.setText(tag)
        self.input_password.clear()

    def save_user(self):
        if not self.is_admin_level1:
            return
        if not hasattr(self, "_selected_id"):
            return
        password = self.input_password.text()
        if not password:
            QMessageBox.warning(self, "Dados invÃ¡lidos", "Informe a senha para atualizar.")
            return
        AuthService.update_user(
            self._selected_id,
            self.input_username.text().strip(),
            self.input_name.text().strip(),
            password,
            self.combo_position.currentText(),
            int(self.combo_level.currentText()),
            self.input_tag.text().strip(),
        )
        LogService.log_event(
            "USER_UPDATE",
            f"id_user={self._selected_id} username={self.input_username.text().strip()}",
            self.current_user,
        )
        QMessageBox.information(self, "Atualizado", "UsuÃ¡rio atualizado.")
        self.load_users()

    def delete_user(self):
        if not self.is_admin_level1:
            return
        if not hasattr(self, "_selected_id"):
            return
        confirm = QMessageBox.question(
            self,
            "Confirmar exclusÃ£o",
            "Deseja excluir este usuÃ¡rio?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return
        AuthService.delete_user(self._selected_id)
        LogService.log_event(
            "USER_DELETE",
            f"id_user={self._selected_id}",
            self.current_user,
        )
        QMessageBox.information(self, "ExcluÃ­do", "UsuÃ¡rio excluÃ­do.")
        self.load_users()

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

    # ============================================================
    #  RELATORIO (DASHBOARD)
    # ============================================================
    def show_report_page(self):
        self.ui.pages_stack.setCurrentWidget(self.ui.page_relatorio)
        self.update_report()

    # ============================================================
    #  IMPRESSÃƒO â€“ RELATÃ“RIO COMPLETO DE ESTOQUE
    # ============================================================
    def print_stock_report(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec() != QDialog.Accepted:
            return

        html = self.build_stock_report_html()
        doc = QTextDocument()
        doc.setHtml(html)
        doc.print_(printer)

    def export_stock_report_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exportar PDF", "", "PDF (*.pdf)"
        )
        if not file_path:
            return

        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_path)

        html = self.build_stock_report_html()
        doc = QTextDocument()
        doc.setHtml(html)
        doc.print_(printer)

        QMessageBox.information(self, "Exportar", "PDF gerado com sucesso.")

    def build_stock_report_html(self):
        # Dados
        materials = MaterialService.get_materials(
            category_tag=None,
            description=None,
            item_number=None,
            product=None,
            category=None,
        )
        actions = ActionService.list_actions()

        # Totais
        total_stock = sum(float(r[4]) for r in materials) if materials else 0
        total_out = sum((a[9] or 0) for a in actions if a[0].startswith("ACS"))
        total_in = sum((a[9] or 0) for a in actions if a[0].startswith("ACE"))

        # Itens mais pegos (saÃ­das)
        picked = {}
        for a in actions:
            if not a[0].startswith("ACS"):
                continue
            descr = a[8]
            qty = a[9] or 0
            picked[descr] = picked.get(descr, 0) + qty
        top_picked = sorted(picked.items(), key=lambda x: x[1], reverse=True)[:10]

        # Logo
        logo_path = (Path(__file__).resolve().parents[2] / "assets" / "logo_secretaria.png")
        logo_uri = logo_path.as_uri()

        def row_material(m):
            qty = float(m[4])
            color = "color:#B00020; font-weight:bold;" if qty < 10 else ""
            return f"""
                <tr>
                    <td>{m[0]}</td>
                    <td>{m[1]}</td>
                    <td>{m[2]}</td>
                    <td>{m[3]}</td>
                    <td style="{color}">{qty}</td>
                    <td>{m[5]}</td>
                </tr>
            """

        def row_action(a):
            return f"""
                <tr>
                    <td>{a[0]}</td>
                    <td>{a[3]}</td>
                    <td>{a[6]}</td>
                    <td>{a[7]}</td>
                    <td>{a[8]}</td>
                    <td>{a[9]}</td>
                    <td>{a[10] or ""}</td>
                </tr>
            """

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #3A1A5E; font-size: 14px; }}
                h1 {{ color: #3E0F63; font-size: 24px; }}
                h2 {{ color: #3E0F63; font-size: 18px; margin-top: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th, td {{ border: 1px solid #CBB2E6; padding: 8px; font-size: 14px; }}
                th {{ background: #E6D9F2; color: #3E0F63; }}
                .kpi {{ margin: 8px 0; font-size: 15px; }}
            </style>
        </head>
        <body>
            <div style="display:flex; align-items:center; gap:12px;">
                <img src="{logo_uri}" width="120"/>
                <div>
                    <h1>RelatÃ³rio Completo de Estoque</h1>
                    <div>{datetime.now().strftime("%d/%m/%Y %H:%M")}</div>
                </div>
            </div>

            <div class="kpi"><b>QNT. TOTAL DE ITENS:</b> {int(total_stock)}</div>
            <div class="kpi"><b>QNT. ITENS SAIU:</b> {int(total_out)}</div>
            <div class="kpi"><b>QNT. ITENS CHEGOU:</b> {int(total_in)}</div>

            <h2>Estoque Atual (itens com quantidade abaixo de 10 em vermelho)</h2>
            <table>
                <tr>
                    <th>NÃºmero</th><th>DescriÃ§Ã£o</th><th>Produto</th>
                    <th>Categoria</th><th>Quantidade</th><th>Un.</th>
                </tr>
                {''.join(row_material(m) for m in materials)}
            </table>

            <h2>AÃ§Ãµes (Entradas e Saidas)</h2>
            <table>
                <tr>
                    <th>ID AÃ§Ã£o</th><th>Categoria</th><th>Data</th>
                    <th>ID Item</th><th>DescriÃ§Ã£o</th><th>Quantidade</th><th>Status</th>
                </tr>
                {''.join(row_action(a) for a in actions)}
            </table>

            <h2>Itens Mais Pegos (Saidas)</h2>
            <table>
                <tr><th>DescriÃ§Ã£o</th><th>Quantidade</th></tr>
                {''.join(f"<tr><td>{d}</td><td>{q}</td></tr>" for d,q in top_picked)}
            </table>
        </body>
        </html>
        """
        return html

    def setup_report_form(self):
        self.ui.report_combo_month.clear()
        self.ui.report_combo_month.addItems([
            "Todos",
            "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ])

        self.ui.report_combo_category.clear()
        self.ui.report_combo_category.addItems([
            "Todos",
            "Limpeza, Higiene e Alimentos",
            "Eletrica",
            "Hidraulica",
            "Ferramentas Gerais",
            "Automoveis",
        ])

        self.ui.report_combo_type.clear()
        self.ui.report_combo_type.addItems(["Retirada", "Chegada"])

        self.ui.report_combo_period.clear()
        self.ui.report_combo_period.addItems([
            "Diario", "Semanal", "Mensal", "Trimestral", "Semestral"
        ])

        self.ui.report_combo_month.currentTextChanged.connect(self.update_report)
        self.ui.report_combo_category.currentTextChanged.connect(self.update_report)
        self.ui.report_combo_type.currentTextChanged.connect(self.update_report)
        self.ui.report_combo_period.currentTextChanged.connect(self.update_report)

    def update_report(self):
        actions = self.load_actions_report()
        materials = self.load_materials_report()

        total_items = sum([float(r[4]) for r in materials]) if materials else 0
        self.ui.lbl_total_items.setText(str(int(total_items)))

        items_out = sum((a[5] or 0) for a in actions if a[0].startswith("ACS"))
        items_in = sum((a[5] or 0) for a in actions if a[0].startswith("ACE"))
        self.ui.lbl_items_out.setText(str(int(items_out)))
        self.ui.lbl_items_in.setText(str(int(items_in)))

        report_type = self.ui.report_combo_type.currentText()
        if report_type == "Chegada":
            self.ui.report_chart_title.setText("QNT. ITENS CHEGARAM NA SEMANA")
            self.ui.report_top_title.setText("ITENS MAIS CHEGARAM")
            item = max(materials, key=lambda r: r[4], default=None)
            self.ui.lbl_stock_item.setText(item[1] if item else "-")
            self.ui.lbl_stock_item.setToolTip(item[1] if item else "")
        else:
            self.ui.report_chart_title.setText("QNT. ITENS RETIRADOS NA SEMANA")
            self.ui.report_top_title.setText("ITENS MAIS SÃƒO RETIRADOS")
            item = min(materials, key=lambda r: r[4], default=None)
            self.ui.lbl_stock_item.setText(item[1] if item else "-")
            self.ui.lbl_stock_item.setToolTip(item[1] if item else "")

        self.update_top_items(actions)
        self.update_chart(actions)

    def load_actions_report(self):
        rows = ActionService.list_actions()
        data = []
        for r in rows:
            data.append((r[0], r[3], r[6], r[7], r[8], r[9]))

        category = self.ui.report_combo_category.currentText()
        if category != "Todos":
            data = [r for r in data if category.lower() in (r[1] or "").lower()]

        month = self.ui.report_combo_month.currentText()
        if month != "Todos":
            month_map = {
                "Janeiro": 1, "Fevereiro": 2, "Marco": 3, "Abril": 4, "Maio": 5, "Junho": 6,
                "Julho": 7, "Agosto": 8, "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
            }
            target = month_map.get(month)
            if target:
                data = [r for r in data if self._date_month(r[2]) == target]

        return data

    def load_materials_report(self):
        category = self.ui.report_combo_category.currentText()
        tag_map = {
            "Limpeza, Higiene e Alimentos": "LIM",
            "Eletrica": "ELE",
            "Hidraulica": "HID",
            "Ferramentas Gerais": "FER",
            "Automoveis": "AUT",
        }
        tag = tag_map.get(category) if category != "Todos" else None

        rows = MaterialService.get_materials(
            category_tag=tag,
            description=None,
            item_number=None,
            product=None,
            category=None,
        )
        return rows

    def update_top_items(self, actions):
        report_type = self.ui.report_combo_type.currentText()
        prefix = "ACE" if report_type == "Chegada" else "ACS"
        items = {}
        for id_action, _category, _date, _id_item, descr, qty in actions:
            if not id_action.startswith(prefix):
                continue
            items[descr] = items.get(descr, 0) + (qty or 0)

        top = sorted(items.items(), key=lambda x: x[1], reverse=True)[:5]

        table = self.ui.report_top_items
        table.setRowCount(0)
        if not top:
            return
        table.setRowCount(len(top))
        for i, (descr, _qty) in enumerate(top):
            text = descr if len(descr) <= 18 else descr[:18] + "..."
            item = QTableWidgetItem(text)
            item.setToolTip(descr)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            table.setItem(i, 0, item)

    def update_chart(self, actions):
        report_type = self.ui.report_combo_type.currentText()
        prefix = "ACE" if report_type == "Chegada" else "ACS"
        period = self.ui.report_combo_period.currentText()

        days_map = {
            "Diario": 1,
            "Semanal": 7,
            "Mensal": 30,
            "Trimestral": 90,
            "Semestral": 180,
        }
        days = days_map.get(period, 7)
        end = datetime.now()
        start = end - timedelta(days=days)

        buckets = {}
        for id_action, _category, date_str, _id_item, _descr, qty in actions:
            if not id_action.startswith(prefix):
                continue
            dt = self._parse_date(date_str)
            if not dt:
                continue
            if dt < start or dt > end:
                continue
            key = dt.strftime("%d/%m")
            buckets[key] = buckets.get(key, 0) + (qty or 0)

        labels = list(buckets.keys())
        values = [buckets[k] for k in labels]

        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            self.ui.report_chart.setText("Instale matplotlib para exibir o grÃ¡fico.")
            return

        fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
        ax.bar(labels, values, color="#9B3D97")
        ax.set_ylabel("Quantidade")
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.ui.report_chart.setPixmap(pixmap)
        self.ui.report_chart.setText("")

    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except (TypeError, ValueError):
            return None

    def _date_month(self, date_str):
        dt = self._parse_date(date_str)
        return dt.month if dt else None


class AddMaterialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastrar Item")
        self.setMinimumWidth(480)
        self.setStyleSheet("background-color: #E8E2EE;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        label_style = "font-size: 12px; font-weight: bold; color: #3A1A5E;"
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
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        self.input_id = QLineEdit()
        self.input_id.setStyleSheet(line_style)
        self.input_id.setReadOnly(True)
        self.input_desc = QLineEdit()
        self.input_desc.setStyleSheet(line_style)
        self.input_product = QLineEdit()
        self.input_product.setStyleSheet(line_style)
        self.combo_category = QComboBox()
        self.combo_category.setStyleSheet(combo_style)
        self.combo_category.addItems([
            "Selecione",
            "Limpeza, Higiene e Alimentos",
            "Eletrica",
            "Hidraulica",
            "Ferramentas Gerais",
            "Automoveis",
        ])
        self.input_quantity = QLineEdit()
        self.input_quantity.setStyleSheet(line_style)
        self.input_unit = QLineEdit()
        self.input_unit.setStyleSheet(line_style)

        lbl_id = QLabel("Numero Item")
        lbl_id.setStyleSheet(label_style)
        lbl_desc = QLabel("Descricao")
        lbl_desc.setStyleSheet(label_style)
        lbl_product = QLabel("Produto")
        lbl_product.setStyleSheet(label_style)
        lbl_category = QLabel("Categoria")
        lbl_category.setStyleSheet(label_style)
        lbl_qty = QLabel("Quantidade")
        lbl_qty.setStyleSheet(label_style)
        lbl_unit = QLabel("Un. Medida")
        lbl_unit.setStyleSheet(label_style)

        grid.addWidget(lbl_id, 0, 0)
        grid.addWidget(self.input_id, 1, 0)
        grid.addWidget(lbl_desc, 0, 1)
        grid.addWidget(self.input_desc, 1, 1)
        grid.addWidget(lbl_product, 2, 0)
        grid.addWidget(self.input_product, 3, 0)
        grid.addWidget(lbl_category, 2, 1)
        grid.addWidget(self.combo_category, 3, 1)
        grid.addWidget(lbl_qty, 4, 0)
        grid.addWidget(self.input_quantity, 5, 0)
        grid.addWidget(lbl_unit, 4, 1)
        grid.addWidget(self.input_unit, 5, 1)

        layout.addLayout(grid)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.btn_cancel = QPushButton("CANCELAR")
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #B5B1C2;
                color: #3A1A5E;
                font-size: 13px;
                font-weight: bold;
                border-radius: 10px;
                padding: 6px 18px;
            }
            QPushButton:hover {
                background-color: #9E99AF;
            }
        """)
        self.btn_save = QPushButton("SALVAR")
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #3E0F63;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border-radius: 10px;
                padding: 6px 18px;
            }
            QPushButton:hover {
                background-color: #53207E;
            }
        """)
        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_save)
        layout.addLayout(btn_row)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.save)

        self.combo_category.currentTextChanged.connect(self.update_auto_id)

    def save(self):
        id_item = self.input_id.text().strip()
        descr = self.input_desc.text().strip()
        product = self.input_product.text().strip()
        category = self.combo_category.currentText()
        qty_text = self.input_quantity.text().strip()
        unit = self.input_unit.text().strip()

        if not id_item or not descr or not product or category == "Selecione":
            QMessageBox.warning(self, "Dados invalidos", "Preencha todos os campos obrigatorios.")
            return
        try:
            qty = float(qty_text.replace(",", ".")) if qty_text else 0
        except ValueError:
            QMessageBox.warning(self, "Dados invalidos", "Quantidade invalida.")
            return
        if qty <= 0:
            QMessageBox.warning(self, "Dados invalidos", "Quantidade deve ser maior que zero.")
            return

        self.item_data = {
            "id_item_preview": id_item,
            "descr": descr,
            "product": product,
            "category": category,
            "qty": qty,
            "unit": unit,
        }
        self.accept()

    def update_auto_id(self):
        tag_map = {
            "Limpeza, Higiene e Alimentos": "L",
            "Eletrica": "E",
            "Hidraulica": "H",
            "Ferramentas Gerais": "F",
            "Automoveis": "A",
        }
        category = self.combo_category.currentText()
        prefix = tag_map.get(category)
        if not prefix:
            self.input_id.clear()
            return
        next_id = MaterialService.get_next_item_id(prefix)
        self.input_id.setText(next_id)

    def apply_action_to_stock(self):
        """
        Atualiza o estoque conforme o tipo da aÃ§Ã£o:
        ACE -> entrada (soma)
        ACS -> saÃ­da (subtrai)
        """
        if not self._current_action:
            QMessageBox.warning(
                self,
                "AÃ§Ã£o invÃ¡lida",
                "NÃ£o hÃ¡ aÃ§Ã£o carregada para atualizar o estoque."
            )
            return False

        id_item = (self._current_action.get("id_item") or "").strip()
        quantity = self._current_action.get("quantity")
        id_action = (self._current_action.get("id_action") or "").strip()

        if not id_item:
            QMessageBox.warning(
                self,
                "Item nÃ£o informado",
                "A aÃ§Ã£o nÃ£o possui nÃºmero de item para atualizar o estoque."
            )
            return False

        if quantity is None:
            QMessageBox.warning(
                self,
                "Quantidade invÃ¡lida",
                "A aÃ§Ã£o nÃ£o possui quantidade informada."
            )
            return False

        try:
            qty_value = float(quantity)
        except (TypeError, ValueError):
            QMessageBox.warning(
                self,
                "Quantidade invÃ¡lida",
                "A quantidade da aÃ§Ã£o nÃ£o Ã© numÃ©rica."
            )
            return False

        if qty_value <= 0:
            QMessageBox.warning(
                self,
                "Quantidade invÃ¡lida",
                "A quantidade deve ser maior que zero."
            )
            return False

        # Define o delta conforme o tipo da aÃ§Ã£o
        if id_action.startswith("ACE"):
            delta = qty_value
        else:
            # padrÃ£o: ACS (saÃ­da)
            delta = -qty_value

        ok, message, _new_qty = MaterialService.update_material_quantity(
            id_item, delta
        )
        if not ok:
            QMessageBox.warning(self, "Falha ao atualizar", message)
            return False

        return True
    # ============================================================
    #  NAVEGAÃ‡ÃƒO
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

    def open_help(self):
        from help import HelpWindow
        self.help = HelpWindow()
        self.help.show()
        self.close()

    # ============================================================
    #  RELATORIO (DASHBOARD)
    # ============================================================
    def show_report_page(self):
        self.ui.pages_stack.setCurrentWidget(self.ui.page_relatorio)
        self.update_report()

    def setup_report_form(self):
        # Meses
        self.ui.report_combo_month.clear()
        self.ui.report_combo_month.addItems([
            "Todos",
            "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ])

        # Categoria
        self.ui.report_combo_category.clear()
        self.ui.report_combo_category.addItems([
            "Todos",
            "Limpeza, Higiene e Alimentos",
            "Eletrica",
            "Hidraulica",
            "Ferramentas Gerais",
            "Automoveis",
        ])

        # Tipo
        self.ui.report_combo_type.clear()
        self.ui.report_combo_type.addItems(["Retirada", "Chegada"])

        # Periodo
        self.ui.report_combo_period.clear()
        self.ui.report_combo_period.addItems([
            "Diario", "Semanal", "Mensal", "Trimestral", "Semestral"
        ])

        self.ui.report_combo_month.currentTextChanged.connect(self.update_report)
        self.ui.report_combo_category.currentTextChanged.connect(self.update_report)
        self.ui.report_combo_type.currentTextChanged.connect(self.update_report)
        self.ui.report_combo_period.currentTextChanged.connect(self.update_report)

    def update_report(self):
        actions = self.load_actions_report()
        materials = self.load_materials_report()

        total_items = sum([float(r[4]) for r in materials]) if materials else 0
        self.ui.lbl_total_items.setText(str(int(total_items)))

        items_out = sum((a[5] or 0) for a in actions if a[0].startswith("ACS"))
        items_in = sum((a[5] or 0) for a in actions if a[0].startswith("ACE"))
        self.ui.lbl_items_out.setText(str(int(items_out)))
        self.ui.lbl_items_in.setText(str(int(items_in)))

        report_type = self.ui.report_combo_type.currentText()
        if report_type == "Chegada":
            self.ui.report_chart_title.setText("QNT. ITENS CHEGARAM NA SEMANA")
            self.ui.report_top_title.setText("ITENS MAIS CHEGARAM")
            item = max(materials, key=lambda r: r[4], default=None)
            self.ui.lbl_stock_item.setText(item[1] if item else "-")
            self.ui.lbl_stock_item.setToolTip(item[1] if item else "")
        else:
            self.ui.report_chart_title.setText("QNT. ITENS RETIRADOS NA SEMANA")
            self.ui.report_top_title.setText("ITENS MAIS SÃƒO RETIRADOS")
            item = min(materials, key=lambda r: r[4], default=None)
            self.ui.lbl_stock_item.setText(item[1] if item else "-")
            self.ui.lbl_stock_item.setToolTip(item[1] if item else "")

        self.update_top_items(actions)
        self.update_chart(actions)

    def load_actions_report(self):
        rows = ActionService.list_actions()
        # map to tuple: (id_action, category, date, id_item, descr, qty)
        data = []
        for r in rows:
            data.append((r[0], r[3], r[6], r[7], r[8], r[9]))

        # filtros
        category = self.ui.report_combo_category.currentText()
        if category != "Todos":
            data = [r for r in data if category.lower() in (r[1] or "").lower()]

        month = self.ui.report_combo_month.currentText()
        if month != "Todos":
            month_map = {
                "Janeiro": 1, "Fevereiro": 2, "Marco": 3, "Abril": 4, "Maio": 5, "Junho": 6,
                "Julho": 7, "Agosto": 8, "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
            }
            target = month_map.get(month)
            if target:
                data = [r for r in data if self._date_month(r[2]) == target]

        return data

    def load_materials_report(self):
        category = self.ui.report_combo_category.currentText()
        tag_map = {
            "Limpeza, Higiene e Alimentos": "LIM",
            "Eletrica": "ELE",
            "Hidraulica": "HID",
            "Ferramentas Gerais": "FER",
            "Automoveis": "AUT",
        }
        tag = tag_map.get(category) if category != "Todos" else None

        rows = MaterialService.get_materials(
            category_tag=tag,
            description=None,
            item_number=None,
            product=None,
            category=None,
        )
        return rows

    def update_top_items(self, actions):
        report_type = self.ui.report_combo_type.currentText()
        prefix = "ACE" if report_type == "Chegada" else "ACS"
        items = {}
        for id_action, _category, _date, _id_item, descr, qty in actions:
            if not id_action.startswith(prefix):
                continue
            items[descr] = items.get(descr, 0) + (qty or 0)

        top = sorted(items.items(), key=lambda x: x[1], reverse=True)[:5]

        table = self.ui.report_top_items
        table.setRowCount(0)
        if not top:
            return
        table.setRowCount(len(top))
        for i, (descr, _qty) in enumerate(top):
            text = descr if len(descr) <= 18 else descr[:18] + "..."
            item = QTableWidgetItem(text)
            item.setToolTip(descr)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            table.setItem(i, 0, item)

    def update_chart(self, actions):
        report_type = self.ui.report_combo_type.currentText()
        prefix = "ACE" if report_type == "Chegada" else "ACS"
        period = self.ui.report_combo_period.currentText()

        # window length
        days_map = {
            "Diario": 1,
            "Semanal": 7,
            "Mensal": 30,
            "Trimestral": 90,
            "Semestral": 180,
        }
        days = days_map.get(period, 7)
        end = datetime.now()
        start = end - timedelta(days=days)

        buckets = {}
        for id_action, _category, date_str, _id_item, _descr, qty in actions:
            if not id_action.startswith(prefix):
                continue
            dt = self._parse_date(date_str)
            if not dt:
                continue
            if dt < start or dt > end:
                continue
            key = dt.strftime("%d/%m")
            buckets[key] = buckets.get(key, 0) + (qty or 0)

        labels = list(buckets.keys())
        values = [buckets[k] for k in labels]

        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            self.ui.report_chart.setText("Instale matplotlib para exibir o grÃ¡fico.")
            return

        fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
        ax.bar(labels, values, color="#9B3D97")
        ax.set_ylabel("Quantidade")
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.ui.report_chart.setPixmap(pixmap)
        self.ui.report_chart.setText("")

    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except (TypeError, ValueError):
            return None

    def _date_month(self, date_str):
        dt = self._parse_date(date_str)
        return dt.month if dt else None

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
        LogService.log_event(
            "USER_CREATE",
            f"username={username} position={position_text} level={level_value} tag={tag}",
            self.user,
        )
        LogService.log_event(
            "USER_CREATE",
            f"username={username} position={position_text} level={level_value} tag={tag}",
            self.user,
        )
        QMessageBox.information(self, "Cadastro", "Usuario cadastrado com sucesso.")
        self.clear_employee_form()



















