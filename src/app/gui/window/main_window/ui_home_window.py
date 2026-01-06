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

# IMPORT LIBRARIES
import os
from gui import resources_rc

# MENU CARD
class MenuCard(QFrame):
    def __init__(self, icon_resource, text):
        super().__init__()

        self.setFixedSize(260, 220)

        self.setStyleSheet("""
            QFrame {
                background-color: #D8CFE2;
                border-radius: 20px;
            }
            QFrame:hover {
                background-color: #D1C6DF;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)

        # ICON
        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setPixmap(
            QPixmap(icon_resource).scaled(
                100, 100,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        # TEXT
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("""
            QLabel {
                color: #390E68;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        layout.addWidget(self.icon)
        layout.addWidget(self.label)

# HOME WINDOW
class UI_HomeWindow(object):
  def setup_ui(self, parent):
    if not parent.objectName():
      parent.setObjectName("HomeWindow") 
       
      # INICIAL    
      parent.resize(1200, 720)
      parent.setMinimumSize(960, 540)

      parent.setWindowTitle("Almoxarifado Obras - Inicial")
      parent.setWindowIcon(QIcon("assets/icon.jpg"))
      parent.setStyleSheet("background-color: #E8E2EE;")

    # CENTRAL WIDGET
    self.central_widget = QWidget(parent)
    parent.setCentralWidget(self.central_widget)

    main_layout = QVBoxLayout(self.central_widget)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)

    # TOP BAR
    self.top_bar = QFrame()
    self.top_bar.setFixedHeight(50)
    self.top_bar.setStyleSheet("background-color: #390E68;")

    top_layout = QHBoxLayout(self.top_bar)
    top_layout.setContentsMargins(20, 0, 20, 0)

    self.btn_sair = QPushButton("  Sair")
    self.btn_sair.setIcon(QIcon("assets/exit.png"))
    self.btn_sair.setStyleSheet(self.top_button_style())

    self.btn_perfil = QPushButton("  Meu perfil")
    self.btn_perfil.setIcon(QIcon("assets/user_profile.png"))
    self.btn_perfil.setStyleSheet(self.top_button_style())

    top_layout.addWidget(self.btn_sair)
    top_layout.addStretch()
    top_layout.addWidget(self.btn_perfil)

    main_layout.addWidget(self.top_bar)

    # CONTENT
    self.content = QWidget()
    grid = QGridLayout(self.content)
    grid.setSpacing(40)
    grid.setContentsMargins(60, 40, 60, 40)

    cards = [
            ("assets/cleaning_tools.png", "Limpeza, Higiene &\nAlimentos"),
            ("assets/wiring.png", "Elétrica"),
            ("assets/hydraulic.png", "Hidráulica"),
            ("assets/tools.png", "Ferramentas Gerais"),
            ("assets/box-truck.png", "Automóveis"),
            ("assets/database.png", "Base de dados dos\nColaboradores"),
            ("assets/help.png", "Ajuda"),
        ]

    row = col = 0
    for icon, text in cards:
        card = MenuCard(icon, text)
        grid.addWidget(card, row, col)

        col += 1
        if col == 4:
                col = 0
                row += 1

    main_layout.addWidget(self.content)

  # STYLES
  def top_button_style(self):
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