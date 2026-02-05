"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    Screen to control fuel supply for work vehicles.
====================================================================
"""

from qt_core import *

from gui.window.main_window.ui_control_gas_window import UI_ControlGasWindow
from gui.window.main_window.ui_control_gas_form_window import UI_ControlGasFormWindow
from gui.window.main_window.ui_control_gas_vehicle_window import UI_ControlGasVehicleWindow
from gui.window.main_window.ui_control_gas_detail_window import UI_ControlGasDetailWindow
from auth.session import Session
from vehicle_service import VehicleService
from control_gas_service import ControlGasService


class ControlGasWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Sessão
        if not Session.is_authenticated():
            self.close()
            return

        self.user = Session.get()

        # UI
        self.ui = UI_ControlGasWindow()
        self.ui.setup_ui(self)

        # Conexões
        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)

        self.ui.btn_filter.clicked.connect(self.apply_filters)
        self.ui.btn_print.clicked.connect(self.print_report)
        self.ui.btn_export.clicked.connect(self.export_report)
        self.ui.btn_tool_add_file.clicked.connect(self.open_gas_form)
        self.ui.btn_tool_remove_file.clicked.connect(self.open_gas_delete)
        self.ui.btn_tool_write.clicked.connect(self.open_gas_edit)
        self.ui.btn_tool_add_car.clicked.connect(self.open_vehicle_form)
        self.ui.btn_tool_remove_car.clicked.connect(self.open_vehicle_delete)
        self.ui.btn_tool_edit_car.clicked.connect(self.open_vehicle_edit)

        self._controls = []
        self.ui.table_gas.setSelectionBehavior(QTableWidget.SelectRows)
        self.ui.table_gas.setSelectionMode(QTableWidget.SingleSelection)
        self.ui.table_gas.cellDoubleClicked.connect(self.open_control_detail)

        self.load_control_filters()
        self.load_controls()

        self.show()

    def apply_filters(self):
        name_vehicle = self.ui.input_vehicle.text().strip()
        plate = self.ui.input_plate.text().strip()
        driver = self.ui.input_driver.text().strip()
        fuel_type = self.ui.combo_fuel.currentText()
        date_str = self.ui.input_date.text().strip()

        rows = ControlGasService.list_controls(
            name_vehicle=name_vehicle or None,
            plate_number=plate or None,
            driver=driver or None,
            fuel_type=fuel_type or None,
            date_str=date_str or None,
        )
        self.populate_control_table(rows)

    def print_report(self):
        # Placeholder: implementar impressão
        pass

    def export_report(self):
        # Placeholder: implementar exportação
        pass

    def open_gas_form(self):
        self.form = ControlGasFormWindow(action_mode="register")
        self.form.show()
        self.close()

    def open_gas_delete(self):
        selected = self.get_selected_control()
        if not selected:
            QMessageBox.warning(self, "Seleção", "Selecione um abastecimento na tabela.")
            return
        self.form = ControlGasFormWindow(action_mode="delete", control_data=selected)
        self.form.show()
        self.close()

    def open_gas_edit(self):
        selected = self.get_selected_control()
        if not selected:
            QMessageBox.warning(self, "Seleção", "Selecione um abastecimento na tabela.")
            return
        self.form = ControlGasFormWindow(action_mode="edit", control_data=selected)
        self.form.show()
        self.close()

    def open_vehicle_form(self):
        self.vehicle_form = ControlGasVehicleWindow(action_mode="register")
        self.vehicle_form.show()
        self.close()

    def open_vehicle_delete(self):
        self.vehicle_form = ControlGasVehicleWindow(action_mode="delete")
        self.vehicle_form.show()
        self.close()

    def open_vehicle_edit(self):
        self.vehicle_form = ControlGasVehicleWindow(action_mode="edit")
        self.vehicle_form.show()
        self.close()

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

    def load_control_filters(self):
        self.ui.combo_fuel.clear()
        self.ui.combo_fuel.addItem("Selecione")
        for value in ControlGasService.get_distinct_fuel_types():
            self.ui.combo_fuel.addItem(str(value))

    def load_controls(self):
        rows = ControlGasService.list_controls()
        self.populate_control_table(rows)

    def populate_control_table(self, rows):
        self._controls = rows
        table = self.ui.table_gas
        table.setRowCount(0)

        if not rows:
            return

        table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            (
                _id_control,
                name_vehicle,
                plate_numbler,
                date_str,
                driver,
                _odometer_type,
                odometer,
                odometer_diff,
                liters_filled,
                avg_consumption,
                fuel_type,
                value,
            ) = row
            values = [
                name_vehicle,
                plate_numbler,
                date_str,
                driver,
                odometer,
                odometer_diff,
                liters_filled,
                avg_consumption,
                fuel_type,
                value,
            ]
            for col_index, value_item in enumerate(values):
                item = QTableWidgetItem(str(value_item))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                table.setItem(row_index, col_index, item)

    def get_selected_control(self):
        row = self.ui.table_gas.currentRow()
        if row < 0 or row >= len(self._controls):
            return None
        return self._controls[row]

    def open_control_detail(self, row, _column):
        if row < 0 or row >= len(self._controls):
            return
        data = self._controls[row]
        self.detail = ControlGasDetailWindow(data)
        self.detail.show()


class ControlGasDetailWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.ui = UI_ControlGasDetailWindow()
        self.ui.setup_ui(self)

        (
            id_control,
            name_vehicle,
            plate_numbler,
            date_str,
            driver,
            odometer_type,
            odometer,
            odometer_diff,
            liters_filled,
            avg_consumption,
            fuel_type,
            value,
        ) = data

        content = (
            f"ID: {id_control}\n"
            f"Veículo: {name_vehicle}\n"
            f"Placa: {plate_numbler}\n"
            f"Data: {date_str}\n"
            f"Motorista: {driver}\n"
            f"Tipo Odômetro: {odometer_type}\n"
            f"Odômetro: {odometer}\n"
            f"Diferença: {odometer_diff}\n"
            f"Litros abastecidos: {liters_filled}\n"
            f"Média Consumo: {avg_consumption}\n"
            f"Tipo Combustível: {fuel_type}\n"
            f"Valor: {value}"
        )
        self.ui.lbl_content.setText(content)
        self.ui.btn_close.clicked.connect(self.close)


class ControlGasFormWindow(QMainWindow):
    def __init__(self, action_mode="register", control_data=None):
        super().__init__()

        if not Session.is_authenticated():
            self.close()
            return

        self.user = Session.get()

        self.ui = UI_ControlGasFormWindow()
        self.action_mode = action_mode
        self.control_data = control_data
        self.ui.setup_ui(self, action_mode=action_mode)

        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)
        self.ui.btn_cancel.clicked.connect(self.back_to_control)
        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_register.clicked.connect(self.register_form)

        self._vehicles = []
        self._selected_photo_path = None

        self.load_form_data()
        self.ui.combo_car.currentIndexChanged.connect(self.on_vehicle_selected)

        self.show()

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

    def back_to_control(self):
        self.control = ControlGasWindow()
        self.control.show()
        self.close()

    def clear_form(self):
        self.ui.combo_car.setCurrentIndex(0)
        self.ui.combo_plate.setCurrentIndex(0)
        self.ui.combo_odo_type.setCurrentIndex(0)
        self.ui.combo_fuel.setCurrentIndex(0)
        self.ui.input_date.clear()
        self.ui.input_driver.clear()
        self.ui.input_odo.clear()
        self.ui.input_qty.clear()
        self.ui.input_value.clear()
        self._selected_photo_path = None

    def register_form(self):
        if self.action_mode == "delete":
            if not self.control_data:
                QMessageBox.warning(self, "Seleção", "Selecione um abastecimento para deletar.")
                return
            control_id = self.control_data[0]
            confirm = QMessageBox.question(
                self,
                "Confirmar exclusão",
                "Deseja deletar este abastecimento?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirm != QMessageBox.Yes:
                return
            ControlGasService.delete_control(control_id)
            QMessageBox.information(self, "Exclusão", "Abastecimento deletado com sucesso.")
            self.back_to_control()
            return

        name = self.ui.combo_car.currentText().strip()
        plate = self.ui.combo_plate.currentText().strip()
        driver = self.ui.input_driver.text().strip()
        fuel = self.ui.combo_fuel.currentText().strip()
        odometer_text = self.ui.combo_odo_type.currentText().strip()
        odometer_value = self.ui.input_odo.text().strip()
        liters_value = self.ui.input_qty.text().strip()
        value_text = self.ui.input_value.text().strip()
        date_str = self.ui.input_date.text().strip()

        if not name or name == "Selecione":
            QMessageBox.warning(self, "Dados inválidos", "Informe o veículo.")
            return
        if not plate or plate == "Selecione":
            QMessageBox.warning(self, "Dados inválidos", "Informe a placa.")
            return
        if not date_str:
            QMessageBox.warning(self, "Dados inválidos", "Informe a data.")
            return
        if not driver:
            QMessageBox.warning(self, "Dados inválidos", "Informe o motorista.")
            return
        if not fuel or fuel == "Selecione":
            QMessageBox.warning(self, "Dados inválidos", "Selecione o tipo de combustível.")
            return
        if not odometer_text or odometer_text == "Selecione":
            QMessageBox.warning(self, "Dados inválidos", "Selecione o tipo de odômetro.")
            return
        if not odometer_value:
            QMessageBox.warning(self, "Dados inválidos", "Informe o odômetro.")
            return
        if not liters_value:
            QMessageBox.warning(self, "Dados inválidos", "Informe a quantidade abastecida.")
            return
        if not value_text:
            QMessageBox.warning(self, "Dados inválidos", "Informe o valor.")
            return

        try:
            odometer_type = int(odometer_text)
            odometer = float(odometer_value.replace(",", "."))
            liters = float(liters_value.replace(",", "."))
            value = float(value_text.replace(",", "."))
        except ValueError:
            QMessageBox.warning(self, "Dados inválidos", "Valores numéricos inválidos.")
            return

        # Campos derivados (sem UI por enquanto)
        odometer_diff = ""
        avg_consumption = ""

        if self.action_mode == "edit":
            if not self.control_data:
                QMessageBox.warning(self, "Seleção", "Selecione um abastecimento para editar.")
                return
            control_id = self.control_data[0]
            ControlGasService.update_control(
                control_id,
                name,
                plate,
                date_str,
                driver,
                odometer_type,
                odometer,
                odometer_diff,
                liters,
                avg_consumption,
                fuel,
                value,
            )
            QMessageBox.information(self, "Edição", "Abastecimento atualizado com sucesso.")
            self.back_to_control()
            return

        ControlGasService.create_control(
            name,
            plate,
            date_str,
            driver,
            odometer_type,
            odometer,
            odometer_diff,
            liters,
            avg_consumption,
            fuel,
            value,
        )
        QMessageBox.information(self, "Cadastro", "Abastecimento cadastrado com sucesso.")
        self.back_to_control()

    def load_form_data(self):
        # Combos de veículos
        self._vehicles = VehicleService.list_vehicles()
        self.ui.combo_car.clear()
        self.ui.combo_car.addItem("Selecione")
        for v in self._vehicles:
            self.ui.combo_car.addItem(v[1])

        # Combos de placa (preenchidos conforme seleção do veículo)
        self.ui.combo_plate.clear()
        self.ui.combo_plate.addItem("Selecione")

        # Combos de tipos
        self.ui.combo_fuel.clear()
        self.ui.combo_fuel.addItem("Selecione")
        for value in VehicleService.get_distinct_fuel_types():
            self.ui.combo_fuel.addItem(str(value))

        self.ui.combo_odo_type.clear()
        self.ui.combo_odo_type.addItem("Selecione")
        for value in VehicleService.get_distinct_odometer_types():
            self.ui.combo_odo_type.addItem(str(value))

        if self.control_data:
            (
                _id_control,
                name_vehicle,
                plate_number,
                date_str,
                driver,
                odometer_type,
                odometer,
                _odometer_diff,
                liters_filled,
                _avg_consumption,
                fuel_type,
                value,
            ) = self.control_data

            if self.ui.combo_car.findText(name_vehicle) == -1:
                self.ui.combo_car.addItem(name_vehicle)
            self.ui.combo_car.setCurrentText(name_vehicle)

            if self.ui.combo_plate.findText(plate_number) == -1:
                self.ui.combo_plate.addItem(plate_number)
            self.ui.combo_plate.setCurrentText(plate_number)

            if self.ui.combo_fuel.findText(str(fuel_type)) == -1:
                self.ui.combo_fuel.addItem(str(fuel_type))
            self.ui.combo_fuel.setCurrentText(str(fuel_type))

            odometer_text = str(odometer_type)
            if self.ui.combo_odo_type.findText(odometer_text) == -1:
                self.ui.combo_odo_type.addItem(odometer_text)
            self.ui.combo_odo_type.setCurrentText(odometer_text)

            self.ui.input_date.setText(str(date_str or ""))
            self.ui.input_driver.setText(str(driver or ""))
            self.ui.input_odo.setText(str(odometer or ""))
            self.ui.input_qty.setText(str(liters_filled or ""))
            self.ui.input_value.setText(str(value or ""))

        # Mode adjustments
        if self.action_mode == "delete":
            self.set_form_read_only(True)
        else:
            self.set_form_read_only(False)

    def on_vehicle_selected(self):
        idx = self.ui.combo_car.currentIndex() - 1
        if idx < 0 or idx >= len(self._vehicles):
            return
        (
            _id_vehicle,
            name_vehicle,
            plate_number,
            fuel_type,
            odometer_type,
            _image_path,
        ) = self._vehicles[idx]

        if self.ui.combo_plate.findText(plate_number) == -1:
            self.ui.combo_plate.addItem(plate_number)
        self.ui.combo_plate.setCurrentText(plate_number)

        if fuel_type:
            if self.ui.combo_fuel.findText(str(fuel_type)) == -1:
                self.ui.combo_fuel.addItem(str(fuel_type))
            self.ui.combo_fuel.setCurrentText(str(fuel_type))

        if odometer_type is not None:
            odometer_text = str(odometer_type)
            if self.ui.combo_odo_type.findText(odometer_text) == -1:
                self.ui.combo_odo_type.addItem(odometer_text)
            self.ui.combo_odo_type.setCurrentText(odometer_text)

    def set_form_read_only(self, read_only: bool):
        self.ui.combo_car.setEnabled(not read_only)
        self.ui.combo_plate.setEnabled(not read_only)
        self.ui.combo_odo_type.setEnabled(not read_only)
        self.ui.combo_fuel.setEnabled(not read_only)
        self.ui.input_date.setReadOnly(read_only)
        self.ui.input_driver.setReadOnly(read_only)
        self.ui.input_odo.setReadOnly(read_only)
        self.ui.input_qty.setReadOnly(read_only)
        self.ui.input_value.setReadOnly(read_only)


class ControlGasVehicleWindow(QMainWindow):
    def __init__(self, action_mode="register"):
        super().__init__()

        if not Session.is_authenticated():
            self.close()
            return

        self.user = Session.get()

        self.ui = UI_ControlGasVehicleWindow()
        self.action_mode = action_mode
        self.ui.setup_ui(self, action_mode=action_mode)

        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)
        self.ui.btn_cancel.clicked.connect(self.back_to_control)
        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_register.clicked.connect(self.register_form)
        self.ui.btn_photo.clicked.connect(self.select_photo)

        self._vehicles = []
        self._selected_vehicle_id = None
        self._selected_photo_path = None

        self.load_vehicle_data()
        self.ui.combo_car.currentIndexChanged.connect(self.on_vehicle_selected)

        self.show()

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

    def back_to_control(self):
        self.control = ControlGasWindow()
        self.control.show()
        self.close()

    def clear_form(self):
        self._selected_vehicle_id = None
        self._selected_photo_path = None
        self.ui.combo_car.setCurrentIndex(0)
        self.ui.combo_odo_type.setCurrentIndex(0)
        self.ui.combo_fuel.setCurrentIndex(0)
        self.ui.input_plate.clear()

    def register_form(self):
        name = self.ui.combo_car.currentText().strip()
        plate = self.ui.input_plate.text().strip()
        fuel = self.ui.combo_fuel.currentText().strip()
        odometer_text = self.ui.combo_odo_type.currentText().strip()

        if not name or name == "Selecione":
            QMessageBox.warning(self, "Dados inválidos", "Informe o nome do veículo.")
            return
        if not plate:
            QMessageBox.warning(self, "Dados inválidos", "Informe a placa.")
            return
        if not fuel or fuel == "Selecione":
            QMessageBox.warning(self, "Dados inválidos", "Selecione o tipo de combustível.")
            return
        if not odometer_text or odometer_text == "Selecione":
            QMessageBox.warning(self, "Dados inválidos", "Selecione o tipo de odômetro.")
            return

        try:
            odometer_type = int(odometer_text)
        except ValueError:
            QMessageBox.warning(self, "Dados inválidos", "Tipo de odômetro deve ser numérico.")
            return

        if self.action_mode == "delete":
            if not self._selected_vehicle_id:
                QMessageBox.warning(self, "Seleção", "Selecione um veículo para deletar.")
                return
            confirm = QMessageBox.question(
                self,
                "Confirmar exclusão",
                "Deseja deletar este veículo?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirm != QMessageBox.Yes:
                return
            VehicleService.delete_vehicle(self._selected_vehicle_id)
            QMessageBox.information(self, "Exclusão", "Veículo deletado com sucesso.")
            self.back_to_control()
            return

        if self.action_mode == "edit":
            if not self._selected_vehicle_id:
                QMessageBox.warning(self, "Seleção", "Selecione um veículo para editar.")
                return
            VehicleService.update_vehicle(
                self._selected_vehicle_id,
                name,
                plate,
                fuel,
                odometer_type,
                self._selected_photo_path,
            )
            QMessageBox.information(self, "Edição", "Veículo atualizado com sucesso.")
            self.back_to_control()
            return

        VehicleService.create_vehicle(
            name,
            plate,
            fuel,
            odometer_type,
            self._selected_photo_path,
        )
        QMessageBox.information(self, "Cadastro", "Veículo cadastrado com sucesso.")
        self.back_to_control()

    def select_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar foto do veículo",
            "",
            "Imagens (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_path:
            return
        self._selected_photo_path = file_path
        QMessageBox.information(self, "Foto selecionada", "Foto do veículo atualizada.")

    def load_vehicle_data(self):
        # Combos de tipos
        self.ui.combo_fuel.clear()
        self.ui.combo_fuel.addItem("Selecione")
        for value in VehicleService.get_distinct_fuel_types():
            self.ui.combo_fuel.addItem(str(value))

        self.ui.combo_odo_type.clear()
        self.ui.combo_odo_type.addItem("Selecione")
        for value in VehicleService.get_distinct_odometer_types():
            self.ui.combo_odo_type.addItem(str(value))

        # Veículos
        self._vehicles = VehicleService.list_vehicles()
        self.ui.combo_car.clear()
        self.ui.combo_car.addItem("Selecione")
        for v in self._vehicles:
            self.ui.combo_car.addItem(v[1])

        # Modo
        if self.action_mode == "register":
            self.ui.combo_car.setEditable(True)
        else:
            self.ui.combo_car.setEditable(False)

    def on_vehicle_selected(self):
        if self.action_mode == "register":
            return
        idx = self.ui.combo_car.currentIndex() - 1
        if idx < 0 or idx >= len(self._vehicles):
            self._selected_vehicle_id = None
            return

        (
            vehicle_id,
            name,
            plate,
            fuel,
            odometer_type,
            image_path,
        ) = self._vehicles[idx]
        self._selected_vehicle_id = vehicle_id
        self._selected_photo_path = image_path

        self.ui.input_plate.setText(str(plate or ""))

        if fuel:
            if self.ui.combo_fuel.findText(str(fuel)) == -1:
                self.ui.combo_fuel.addItem(str(fuel))
            self.ui.combo_fuel.setCurrentText(str(fuel))

        if odometer_type is not None:
            odometer_text = str(odometer_type)
            if self.ui.combo_odo_type.findText(odometer_text) == -1:
                self.ui.combo_odo_type.addItem(odometer_text)
            self.ui.combo_odo_type.setCurrentText(odometer_text)
