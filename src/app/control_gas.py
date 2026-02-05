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
from auth.session import Session


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
        self.ui.btn_tool_add_car.clicked.connect(self.open_vehicle_form)

        self.show()

    def apply_filters(self):
        # Placeholder: implementar filtro real quando o banco estiver pronto
        pass

    def print_report(self):
        # Placeholder: implementar impressão
        pass

    def export_report(self):
        # Placeholder: implementar exportação
        pass

    def open_gas_form(self):
        self.form = ControlGasFormWindow()
        self.form.show()
        self.close()

    def open_vehicle_form(self):
        self.vehicle_form = ControlGasVehicleWindow()
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


class ControlGasFormWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if not Session.is_authenticated():
            self.close()
            return

        self.user = Session.get()

        self.ui = UI_ControlGasFormWindow()
        self.ui.setup_ui(self)

        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)
        self.ui.btn_cancel.clicked.connect(self.back_to_control)
        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_register.clicked.connect(self.register_form)

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
        self.ui.input_driver.clear()
        self.ui.input_odo.clear()
        self.ui.input_qty.clear()
        self.ui.input_value.clear()

    def register_form(self):
        # Placeholder: salvar no banco
        pass


class ControlGasVehicleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if not Session.is_authenticated():
            self.close()
            return

        self.user = Session.get()

        self.ui = UI_ControlGasVehicleWindow()
        self.ui.setup_ui(self)

        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_profile.clicked.connect(self.open_profile)
        self.ui.btn_cancel.clicked.connect(self.back_to_control)
        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_register.clicked.connect(self.register_form)
        self.ui.btn_photo.clicked.connect(self.select_photo)

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
        self.ui.combo_odo_type.setCurrentIndex(0)
        self.ui.combo_fuel.setCurrentIndex(0)
        self.ui.input_plate.clear()

    def register_form(self):
        # Placeholder: salvar no banco
        pass

    def select_photo(self):
        # Placeholder: selecionar foto do veículo
        pass
