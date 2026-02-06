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

import os
import csv
import io
from datetime import datetime, timedelta
from qt_core import *
from PySide6.QtPrintSupport import QPrinter, QPrintDialog

from gui.window.main_window.ui_control_gas_window import UI_ControlGasWindow
from gui.window.main_window.ui_control_gas_form_window import UI_ControlGasFormWindow
from gui.window.main_window.ui_control_gas_vehicle_window import UI_ControlGasVehicleWindow
from gui.window.main_window.ui_control_gas_detail_window import UI_ControlGasDetailWindow
from gui.window.main_window.ui_control_gas_export_window import UI_ControlGasExportWindow
from gui.window.main_window.ui_control_gas_report_window import UI_ControlGasReportWindow
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
        self.report = ControlGasReportWindow()
        self.report.show()

    def export_report(self):
        self.export = ControlGasExportWindow()
        self.export.show()

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


class ControlGasExportWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if not Session.is_authenticated():
            self.close()
            return

        self.ui = UI_ControlGasExportWindow()
        self.ui.setup_ui(self)

        self.ui.btn_cancel.clicked.connect(self.close)
        self.ui.btn_export.clicked.connect(self.handle_export)

        self.show()

    def handle_export(self):
        period = self.get_selected_period()
        fmt = self.get_selected_format()

        data = self.filter_by_period(period)
        if not data:
            QMessageBox.information(self, "Exportar", "Nenhum registro encontrado.")
            return

        if fmt == "CSV":
            self.export_csv(data)
        else:
            self.export_pdf(data)

    def get_selected_period(self):
        if self.ui.radio_quarterly.isChecked():
            return "quarterly"
        if self.ui.radio_semiannual.isChecked():
            return "semiannual"
        if self.ui.radio_annual.isChecked():
            return "annual"
        return "monthly"

    def get_selected_format(self):
        return "PDF" if self.ui.radio_pdf.isChecked() else "CSV"

    def filter_by_period(self, period):
        end = datetime.now()
        if period == "annual":
            start = end - timedelta(days=365)
        elif period == "semiannual":
            start = end - timedelta(days=182)
        elif period == "quarterly":
            start = end - timedelta(days=91)
        else:
            start = end - timedelta(days=30)

        rows = ControlGasService.list_controls()
        result = []
        for r in rows:
            date_str = r[3]
            try:
                dt = datetime.strptime(date_str, "%d/%m/%Y")
            except (TypeError, ValueError):
                continue
            if start <= dt <= end:
                result.append(r)
        return result

    def export_csv(self, rows):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar CSV", "", "CSV (*.csv)"
        )
        if not file_path:
            return

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "ID",
                "Veiculo",
                "Placa",
                "Data",
                "Motorista",
                "Tipo Odometro",
                "Odometro",
                "Diferenca",
                "Litros",
                "Media",
                "Combustivel",
                "Valor",
            ])
            for r in rows:
                writer.writerow(r)

        QMessageBox.information(self, "Exportar", "CSV gerado com sucesso.")

    def export_pdf(self, rows):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
        except ImportError:
            QMessageBox.warning(
                self,
                "PDF",
                "Dependencia 'reportlab' nao instalada. Use CSV ou instale o pacote.",
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar PDF", "", "PDF (*.pdf)"
        )
        if not file_path:
            return

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y = height - 40

        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, y, "Relatorio de Abastecimento")
        y -= 20
        c.setFont("Helvetica", 9)

        headers = [
            "ID", "Veiculo", "Placa", "Data", "Motorista",
            "Tipo Odo", "Odo", "Dif", "Litros", "Media", "Comb", "Valor"
        ]
        c.drawString(40, y, " | ".join(headers))
        y -= 14

        for r in rows:
            line = " | ".join([str(x) for x in r])
            c.drawString(40, y, line[:200])
            y -= 12
            if y < 40:
                c.showPage()
                y = height - 40
                c.setFont("Helvetica", 9)

        c.save()
        QMessageBox.information(self, "Exportar", "PDF gerado com sucesso.")


class ControlGasReportWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if not Session.is_authenticated():
            self.close()
            return

        self.ui = UI_ControlGasReportWindow()
        self.ui.setup_ui(self)

        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_generate.clicked.connect(self.generate_report)
        self.ui.btn_print.clicked.connect(self.print_report)

        self._last_rows = []
        self.generate_report()
        self.show()

    def get_selected_period(self):
        if self.ui.radio_daily.isChecked():
            return "daily"
        if self.ui.radio_weekly.isChecked():
            return "weekly"
        return "monthly"

    def filter_by_period(self, period):
        end = datetime.now()
        if period == "weekly":
            start = end - timedelta(days=7)
        elif period == "daily":
            start = end - timedelta(days=1)
        else:
            start = end - timedelta(days=30)

        rows = ControlGasService.list_controls()
        result = []
        for r in rows:
            date_str = r[3]
            try:
                dt = datetime.strptime(date_str, "%d/%m/%Y")
            except (TypeError, ValueError):
                continue
            if start <= dt <= end:
                result.append(r)
        return result

    def generate_report(self):
        period = self.get_selected_period()
        rows = self.filter_by_period(period)
        rows = self.filter_by_month(rows)
        self._last_rows = rows

        # Totals
        total_spent = sum(float(r[11]) for r in rows) if rows else 0
        self.ui.lbl_total.setText(f"Total gasto: R$ {total_spent:.2f}")

        # Vehicle most fueled (by liters)
        liters_by_vehicle = {}
        spent_by_vehicle = {}
        count_by_vehicle = {}
        by_plate = {}

        for r in rows:
            vehicle = r[1]
            plate = r[2]
            liters = float(r[8]) if r[8] else 0
            spent = float(r[11]) if r[11] else 0
            avg = float(r[9]) if r[9] else 0
            liters_by_vehicle[vehicle] = liters_by_vehicle.get(vehicle, 0) + liters
            spent_by_vehicle[vehicle] = spent_by_vehicle.get(vehicle, 0) + spent
            count_by_vehicle[vehicle] = count_by_vehicle.get(vehicle, 0) + 1
            if plate not in by_plate:
                by_plate[plate] = {"avg_list": [], "value_list": [], "vehicle": vehicle}
            by_plate[plate]["avg_list"].append(avg)
            by_plate[plate]["value_list"].append(spent)

        top_vehicle = max(liters_by_vehicle, key=liters_by_vehicle.get) if liters_by_vehicle else "-"
        self.ui.lbl_top_vehicle.setText(f"Veiculo que mais abasteceu: {top_vehicle}")

        # Chart
        self.render_chart(count_by_vehicle, spent_by_vehicle)

        # Table summary
        self.populate_summary_table(by_plate)

    def filter_by_month(self, rows):
        month_text = self.ui.combo_month.currentText()
        if month_text == "Todos os meses":
            return rows

        month_map = {
            "Janeiro": 1,
            "Fevereiro": 2,
            "Marco": 3,
            "Abril": 4,
            "Maio": 5,
            "Junho": 6,
            "Julho": 7,
            "Agosto": 8,
            "Setembro": 9,
            "Outubro": 10,
            "Novembro": 11,
            "Dezembro": 12,
        }
        target = month_map.get(month_text)
        if not target:
            return rows

        result = []
        for r in rows:
            date_str = r[3]
            try:
                dt = datetime.strptime(date_str, "%d/%m/%Y")
            except (TypeError, ValueError):
                continue
            if dt.month == target:
                result.append(r)
        return result

    def print_report(self):
        if not self._last_rows:
            QMessageBox.information(self, "Imprimir", "Nenhum dado para imprimir.")
            return

        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec() != QDialog.Accepted:
            return

        text = self.build_print_text(self._last_rows)
        doc = QTextDocument()
        doc.setPlainText(text)
        doc.print_(printer)

    def build_print_text(self, rows):
        by_plate = {}
        total = 0.0
        for r in rows:
            plate = r[2]
            vehicle = r[1]
            date_str = r[3]
            avg = float(r[9]) if r[9] else 0.0
            value = float(r[11]) if r[11] else 0.0

            total += value

            if plate not in by_plate:
                by_plate[plate] = {
                    "vehicle": vehicle,
                    "dates": [],
                    "avg_list": [],
                    "value_sum": 0.0,
                }
            by_plate[plate]["dates"].append(date_str)
            by_plate[plate]["avg_list"].append(avg)
            by_plate[plate]["value_sum"] += value

        lines = []
        lines.append("RELATORIO DE ABASTECIMENTO")
        lines.append("")
        lines.append("Veiculo | Placa | Media | Data | Valor Parcial")
        lines.append("-" * 70)

        for plate, data in by_plate.items():
            avg_list = data["avg_list"]
            avg_consumption = sum(avg_list) / len(avg_list) if avg_list else 0.0
            date_latest = self._latest_date(data["dates"])
            lines.append(
                f"{data['vehicle']} | {plate} | {avg_consumption:.2f} | {date_latest} | {data['value_sum']:.2f}"
            )

        lines.append("-" * 70)
        lines.append(f"TOTAL GASTO: R$ {total:.2f}")
        return "\n".join(lines)

    def _latest_date(self, date_list):
        if not date_list:
            return "-"
        valid = []
        for d in date_list:
            try:
                valid.append(datetime.strptime(d, "%d/%m/%Y"))
            except (TypeError, ValueError):
                continue
        if not valid:
            return "-"
        return max(valid).strftime("%d/%m/%Y")

    def render_chart(self, count_by_vehicle, spent_by_vehicle):
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            self.ui.chart_label.setText("Instale matplotlib para exibir o grafico.")
            return

        vehicles = list(count_by_vehicle.keys())
        counts = [count_by_vehicle[v] for v in vehicles]
        spent = [spent_by_vehicle.get(v, 0) for v in vehicles]

        fig, ax1 = plt.subplots(figsize=(7, 4), dpi=100)
        color1 = "#9B3D97"
        color2 = "#3E0F63"

        ax1.bar(vehicles, counts, color=color1, alpha=0.8, label="Abastecimentos")
        ax1.set_ylabel("Qtde")
        ax1.tick_params(axis="x", rotation=45, labelsize=8)

        ax2 = ax1.twinx()
        ax2.plot(vehicles, spent, color=color2, marker="o", label="Gasto (R$)")
        ax2.set_ylabel("R$")

        fig.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.ui.chart_label.setPixmap(pixmap)
        self.ui.chart_label.setText("")

    def populate_summary_table(self, by_plate):
        table = self.ui.table_summary
        table.setRowCount(0)
        if not by_plate:
            return
        table.setRowCount(len(by_plate))
        for row_idx, (plate, data) in enumerate(by_plate.items()):
            avg_list = data["avg_list"]
            value_list = data["value_list"]
            avg_consumption = sum(avg_list) / len(avg_list) if avg_list else 0
            avg_value = sum(value_list) / len(value_list) if value_list else 0
            for col, val in enumerate([
                plate,
                f"{avg_consumption:.2f}",
                f"{avg_value:.2f}",
            ]):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                table.setItem(row_idx, col, item)


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

        self.ui.val_id.setText(str(id_control))
        self.ui.val_vehicle.setText(str(name_vehicle))
        self.ui.val_plate.setText(str(plate_numbler))
        self.ui.val_date.setText(str(date_str))
        self.ui.val_driver.setText(str(driver))
        self.ui.val_odo_type.setText(str(odometer_type))
        self.ui.val_odo.setText(str(odometer))
        self.ui.val_diff.setText(str(odometer_diff))
        self.ui.val_liters.setText(str(liters_filled))
        self.ui.val_avg.setText(str(avg_consumption))
        self.ui.val_fuel.setText(str(fuel_type))
        self.ui.val_value.setText(str(value))
        self.ui.btn_close.clicked.connect(self.close)

        # Foto do veículo
        vehicle = VehicleService.get_vehicle_by_plate(plate_numbler)
        if vehicle:
            image_path = vehicle[5]
            if image_path and os.path.exists(image_path):
                pixmap = QPixmap(image_path).scaled(
                    self.ui.photo.width(),
                    self.ui.photo.height(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation,
                )
                self.ui.photo.setPixmap(pixmap)
                self.ui.photo.setText("")


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

        # Campos derivados
        last = ControlGasService.get_last_control_by_plate(
            plate_number=plate,
            exclude_id=self.control_data[0] if self.control_data else None
        )
        if last:
            last_odometer = last[6]
            try:
                odometer_diff = float(odometer) - float(last_odometer)
            except (TypeError, ValueError):
                odometer_diff = ""
        else:
            odometer_diff = ""

        if odometer_type == 1:
            # Km/L
            avg_consumption = round(odometer_diff / liters, 2) if odometer_diff else 0
        elif odometer_type == 2:
            # L/h máquina
            avg_consumption = round(liters / odometer_diff, 2) if odometer_diff else 0
        else:
            avg_consumption = 0

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
