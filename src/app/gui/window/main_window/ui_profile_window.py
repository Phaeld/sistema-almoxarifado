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

# HOME WINDOW
class UI_ProfileWindow(object):
  def setup_ui(self, parent):
    if not parent.objectName():
      parent.setObjectName("ProfileWindow") 
       
      # INICIAL    
      parent.resize(1200, 720)
      parent.setMinimumSize(960, 540)

      parent.setWindowTitle("Almoxarifado Obras - Perfil do Usuário")
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

    self.btn_home = QPushButton("  Inicial")
    self.btn_home.setIcon(QIcon("assets/home.png"))
    self.btn_home.setStyleSheet(self.top_button_style())

    self.btn_sair = QPushButton("  Sair")
    self.btn_sair.setIcon(QIcon("assets/exit.png"))
    self.btn_sair.setStyleSheet(self.top_button_style())

    top_layout.addWidget(self.btn_home)
    top_layout.addStretch()
    top_layout.addWidget(self.btn_sair)

    main_layout.addWidget(self.top_bar)

    # CONTENT
    self.content = QWidget()
    grid = QGridLayout(self.content)
    grid.setSpacing(40)
    grid.setContentsMargins(60, 40, 60, 40)

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