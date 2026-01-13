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

    # =============================
    # CONTENT
    # =============================
    content = QWidget()
    content_layout = QHBoxLayout(content)
    content_layout.setContentsMargins(80, 60, 80, 60)
    content_layout.setSpacing(80)

    # =============================
    # PHOTO SECTION
    # =============================
    photo_layout = QVBoxLayout()
    photo_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
    photo_layout.setSpacing(20)

    self.photo = QLabel()
    self.photo.setFixedSize(260, 260)
    self.photo.setStyleSheet("""
        QLabel {
            border-radius: 130px;
            background-color: #D8CFE2;
        }
    """)
    self.photo.setPixmap(
        QPixmap("assets/profile1.png").scaled(
            260, 260, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
    )

    self.btn_change_photo = QPushButton("MUDAR FOTO")
    self.btn_remove_photo = QPushButton("REMOVER FOTO")

    self.btn_change_photo.setStyleSheet(self.primary_button())
    self.btn_remove_photo.setStyleSheet(self.secondary_button())

    photo_layout.addWidget(self.photo)
    photo_layout.addWidget(self.btn_change_photo)
    photo_layout.addWidget(self.btn_remove_photo)


    # INFO SECTION
    info_layout = QVBoxLayout()
    info_layout.setSpacing(25)

    title = QLabel("PERFIL DO USUÁRIO")
    title.setStyleSheet("""
        font-size: 36px;
        font-weight: bold;
        color: #9B4F9A;
    """)

    info_layout.addWidget(title)
    info_layout.addSpacing(20)

    info_layout.addWidget(self.info_block("USUÁRIO", "raphael.silva"))
    info_layout.addWidget(self.info_block("NOME", "RAPHAEL DA SILVA"))

    row = QHBoxLayout()
    row.setSpacing(80)
    row.addWidget(self.info_block("CARGO", "ADMIN", info=True))
    row.addWidget(self.info_block("NÍVEL", "ALTO", info=True))

    info_layout.addLayout(row)
    info_layout.addStretch()

    content_layout.addLayout(photo_layout)
    content_layout.addLayout(info_layout)

    main_layout.addWidget(content)

  # =============================
  # COMPONENTS
  # =============================
  def info_block(self, label_text, value_text, info=False):
      block = QVBoxLayout()
      block.setSpacing(6)

      label = QLabel(label_text)
      label.setStyleSheet("""
            font-size: 14px;
            color: black;
      """)

      value = QLabel(value_text)
      value.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #3E0F63;
      """)

      block.addWidget(label)
      block.addWidget(value)

      container = QWidget()
      container.setLayout(block)
      return container

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

  def primary_button(self):
      return """
            QPushButton {
                background-color: #3E0F63;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 16px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #53207E;
            }
        """

  def secondary_button(self):
      return """
            QPushButton {
                background-color: #A65BB4;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 16px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #8E4AA0;
            }
        """