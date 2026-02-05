# profile.py

from qt_core import *
from gui.window.main_window.ui_profile_window import UI_ProfileWindow
from auth.session import Session
from auth.auth_service import AuthService
import os


class ProfileWindow(QMainWindow):
    def __init__(self, on_logout=None):
        super().__init__()

        self.on_logout = on_logout

        # 🔐 Verifica sessão
        if not Session.is_authenticated():
            self.close()
            return

        # Usuário da sessão
        self.user = Session.get()

        # UI
        self.ui = UI_ProfileWindow()
        self.ui.setup_ui(self)

        # Carrega dados
        self.load_user_data()

        # Conexões
        self.ui.btn_home.clicked.connect(self.go_home)
        self.ui.btn_sair.clicked.connect(self.logout)
        self.ui.btn_change_photo.clicked.connect(self.change_photo)
        self.ui.btn_remove_photo.clicked.connect(self.remove_photo)

    # =============================
    # USER DATA
    # =============================
    def load_user_data(self):
        self.ui.lbl_username.setText(str(self.user.get("username", "")))
        self.ui.lbl_name.setText(str(self.user.get("name", "")))
        self.ui.lbl_position.setText(str(self.user.get("position", "")))

        LEVEL_MAP = {
            0: "BAIXO",
            1: "ALTO"
        }

        level_value = self.user.get("level")
        self.ui.lbl_level.setText(LEVEL_MAP.get(level_value, ""))

        # Foto
        self.load_profile_photo()

    def load_profile_photo(self):
        photo_data = self.user.get("photo")

        pixmap = QPixmap()
        if isinstance(photo_data, (bytes, bytearray, memoryview)):
            if isinstance(photo_data, memoryview):
                photo_data = photo_data.tobytes()
            pixmap.loadFromData(photo_data)
        elif isinstance(photo_data, str) and photo_data and os.path.exists(photo_data):
            pixmap = QPixmap(photo_data)

        if pixmap.isNull():
            pixmap = QPixmap("assets/user_profile.png")

        pixmap = pixmap.scaled(
            260, 260,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        self.ui.photo.setPixmap(pixmap)

    # =============================
    # NAVIGATION
    # =============================
    def go_home(self):
        from home import HomeWindow
        self.home = HomeWindow(on_logout=self.on_logout)
        self.home.show()
        self.close()

    def logout(self):
        Session.end()

        if self.on_logout:
            self.on_logout()

        self.close()

    # =============================
    # ACTIONS
    # =============================
    def change_photo(self):
        username = self.user.get("username")
        if not username:
            QMessageBox.warning(self, "Erro", "Usuário inválido.")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar foto",
            "",
            "Imagens (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_path:
            return

        try:
            with open(file_path, "rb") as f:
                image_bytes = f.read()
        except OSError:
            QMessageBox.warning(self, "Erro", "Não foi possível ler a imagem.")
            return

        AuthService.update_user_image(username, image_bytes)
        self.user["photo"] = image_bytes
        self.load_profile_photo()

        QMessageBox.information(self, "Foto atualizada", "Foto de perfil salva com sucesso.")

    def remove_photo(self):
        username = self.user.get("username")
        if not username:
            QMessageBox.warning(self, "Erro", "Usuário inválido.")
            return

        AuthService.update_user_image(username, None)
        self.user["photo"] = None
        self.load_profile_photo()

        QMessageBox.information(self, "Foto removida", "Foto de perfil removida.")
