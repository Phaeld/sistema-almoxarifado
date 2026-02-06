"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
--------------------------------------------------------------------
    Description:
    This program was developed to manage the internal warehouse
    operations of the company, allowing control of inventory,
    product registrations, incoming and outgoing materials, and
    report generation.

    The system will be implemented in Python using a graphical
    user interface (GUI) and database integration. The goal is to
    provide a practical, intuitive, and efficient solution for the
    management of internally used materials.
====================================================================
"""

# IMPORT QT CORE
from qt_core import *

# MAIN WINDOW
class UI_MainWindow(object):
  def setup_ui(self, parent):
    if not parent.objectName():
      parent.setObjectName("MainWindow") 

      # INICIAL
      parent.resize(1200, 720)
      parent.setMinimumSize(960, 540)
      parent.setStyleSheet("background-color: #E8E2EE;")

      
      parent.setWindowTitle("Almoxarifado Obras - Login")
      parent.setWindowIcon(QIcon("assets/icon.jpg"))

      # WIDGET CENTRAL
      self.central_widget = QWidget()
      parent.setCentralWidget(self.central_widget)
      self.main_layout = QVBoxLayout(self.central_widget)
      self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
      self.main_layout.setContentsMargins(20, 20, 20, 20)

      # NAV BAR
      self.top_bar = QHBoxLayout()
      self.top_bar.setAlignment(Qt.AlignLeft)

      # LOGO 1 (MUNICIPAL GOVERNMENT OF IPAUSSU)
      self.logo1 = QLabel()
      pix1 = QPixmap("assets/logo_pmi.png").scaled(430, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
      self.logo1.setPixmap(pix1)
      self.top_bar.addWidget(self.logo1)
      self.top_bar.addStretch()

      # LOGO 2 (MUNICIPAL SECRETARIAT OF PUBLIC WORKS)
      self.logo2 = QLabel()
      pix2 = QPixmap("assets/logo_secretaria.png").scaled(440, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
      self.logo2.setPixmap(pix2)
      self.top_bar.addWidget(self.logo2)

      self.main_layout.addLayout(self.top_bar)
      self.main_layout.addSpacing(10)

      # TITLE    
      self.title = QLabel("ALMOXARIFADO OBRAS")
      self.title.setAlignment(Qt.AlignCenter)
      self.title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #9b4f9a;
        """)
      self.main_layout.addWidget(self.title)
      self.main_layout.addSpacing(25)

      
      # CARD 
      self.card = QFrame()
      self.card.setObjectName("login_card")
      self.card.setFixedSize(900, 390)

      self.card.setStyleSheet("""
            #login_card {
                background-color: #c3a6e8;
                border-radius: 25px;
            }
        """)

      self.card_layout = QHBoxLayout(self.card)
      self.card_layout.setContentsMargins(40, 40, 40, 40)

      # BACKGROUND ICON
      self.icon_bg = QFrame()
      self.icon_bg.setFixedSize(220, 250)
      self.icon_bg.setStyleSheet("""
            background-color: #c3a6e8;
            border-radius: 15px;
        """)
      self.icon_layout = QVBoxLayout(self.icon_bg)
      self.user_icon = QLabel()
      pix = QPixmap("assets/user_icon.png").scaled(220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)
      self.user_icon.setPixmap(pix)
      self.user_icon.setAlignment(Qt.AlignCenter)
      self.icon_layout.addWidget(self.user_icon)

      self.card_layout.addWidget(self.icon_bg)

      # FORM
      self.form_layout = QVBoxLayout()
      self.form_layout.setSpacing(15)
      self.card_layout.addLayout(self.form_layout)

      # USERNAME
      self.user_label = QLabel("USUÁRIO")
      self.user_label.setStyleSheet("""
            background-color: #c3a6e8;
            padding: 4px;
            border-radius: 6px;
            font-size: 18px; 
            font-weight: bold;
            color: black;
        """)
      self.user_label.setFixedHeight(30)
      self.form_layout.addWidget(self.user_label)

      self.user_input = QLineEdit()
      self.user_input.setPlaceholderText("Digite seu usuário")
      self.user_input.setFixedHeight(45)
      self.user_input.setStyleSheet("""
            background-color: #e8e6e6;
            padding: 10px;
            border-radius: 10px;
            font-size: 16px;
            color: gray;
        """)
      self.form_layout.addWidget(self.user_input)

      # PASSWORD
      self.pass_label = QLabel("SENHA")
      self.pass_label.setStyleSheet("""
            background-color: #c3a6e8;
            padding: 4px;
            border-radius: 6px;
            font-size: 18px; 
            font-weight: bold;
            color: black;
        """)
      self.pass_label.setFixedHeight(30)
      self.form_layout.addWidget(self.pass_label)

      self.pass_input = QLineEdit()
      self.pass_input.setPlaceholderText("Digite sua senha")
      self.pass_input.setEchoMode(QLineEdit.Password)
      self.pass_input.setFixedHeight(45)
      self.pass_input.setStyleSheet("""
            background-color: #e8e6e6;
            padding: 10px;
            border-radius: 10px;
            font-size: 16px;
            color: gray;
        """)
      self.form_layout.addWidget(self.pass_input)

      self.form_layout.addSpacing(20)

      # ERROR LABEL
      self.lbl_error = QLabel("")
      self.lbl_error.setAlignment(Qt.AlignCenter)
      self.lbl_error.setStyleSheet("""
            font-size: 14px;
            color: #7A1E6C;
            font-weight: bold;
      """)
      self.lbl_error.setVisible(False)
      self.form_layout.addWidget(self.lbl_error)

      # SUBMIT BUTTON
      self.login_button = QPushButton("ENTRAR")
      self.login_button.setFixedSize(260, 50)
      self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #5d0c8c;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #6f2aa8;
            }
            QPushButton:pressed {
                background-color: #4b0a70;
            }
        """)

      self.form_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

      # ADD CARD TO SCREEN    
      self.main_layout.addWidget(self.card, alignment=Qt.AlignCenter)
