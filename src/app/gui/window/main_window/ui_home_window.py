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
class UI_HomeWindow(object):
  def setup_ui(self, parent):
    if not parent.objectName():
      parent.setObjectName("HomeWindow") 
        # =============================
        # INICIAL
        # =============================
      parent.resize(1200, 720)
      parent.setMinimumSize(960, 540)
      parent.setStyleSheet("background-color: #E8E2EE;")
