"""
====================================================================
    INTERNAL WAREHOUSE MANAGEMENT SYSTEM
    Author: Raphael da Silva
    Creation Date: 2025
====================================================================
"""

# IMPORT QT CORE
from qt_core import *

# IMPORT RESOURCES
from gui import resources_rc

# ITENS
class QAItem(QWidget):
    def __init__(self, question, answer):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # BUTTON QUESTION
        self.btn = QPushButton(question)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.setCheckable(True)
        self.btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 14px;
                font-size: 18px;
                border: 2px solid #5B2A86;
                border-radius: 10px;
                background-color: transparent;
                color: #4A2A6A;
            }
            QPushButton:checked {
                background-color: #E6D9F2;
            }
        """)

        # ANSWER (HIDDEN)
        self.answer_label = QLabel(answer)
        self.answer_label.setWordWrap(True)
        self.answer_label.setVisible(False)
        self.answer_label.setStyleSheet("""
            QLabel {
                padding: 12px;
                font-size: 18px;
                color: #4A2A6A;
            }
        """)

        self.btn.toggled.connect(self.answer_label.setVisible)

        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.answer_label)

class UI_HelpWindow(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("HelpWindow")

        # WINDOW CONFIG
        parent.resize(1200, 720)
        parent.setMinimumSize(960, 540)
        parent.setWindowTitle("Almoxarifado Obras - Ajuda")
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

        self.btn_profile = QPushButton("  Meu perfil")
        self.btn_profile.setIcon(QIcon("assets/user_profile.png"))
        self.btn_profile.setStyleSheet(self.top_button_style())

        top_layout.addWidget(self.btn_home)
        top_layout.addStretch()
        top_layout.addWidget(self.btn_profile)

        main_layout.addWidget(self.top_bar)
        
        # SCROLL AREA
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        scroll.setWidget(content)

        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(40)

        main_layout.addWidget(scroll)

        # LEFT COLUMN
        left_col = QVBoxLayout()
        left_col.setSpacing(25)

        title = QLabel("AJUDA (HELP) – MANUAL DE USO DO SOFTWARE E Q&A")
        title.setStyleSheet("""
                font-size: 32px;
                font-weight: bold;
                color: #A35CB5;
            """)

        left_col.addWidget(title)

        left_col.addWidget(self.section_title("EXPLICAÇÃO SISTEMA"))
        left_col.addWidget(self.paragraph_text())

        left_col.addWidget(self.section_title("EXPLICAÇÃO TELAS"))
        left_col.addWidget(self.paragraph_text(bold_first=True))

        left_col.addWidget(self.section_title("PERMISSÕES E FERRAMENTAS"))
        left_col.addWidget(self.paragraph_text(bold_first=True))

        left_col.addStretch()

        # RIGHT COLUMN
        right_col = QVBoxLayout()
        right_col.setSpacing(20)
        right_col.setAlignment(Qt.AlignTop)

        text_right = QLabel(
                "Este manual reúne os fluxos principais do sistema, regras de acesso "
                "e boas práticas de uso. Ele é atualizado conforme novas funcionalidades "
                "são entregues."
            )
        text_right.setWordWrap(True)
        text_right.setStyleSheet("""
                font-size: 20px;
                color: #4A2A6A;
            """)

        manual_title = QLabel("BAIXAR MANUAL SOFTWARE PDF")
        manual_title.setStyleSheet("""
                font-size: 26px;
                font-weight: bold;
                color: #5B2A86;
            """)

        manual_img = QLabel()
        manual_img.setPixmap(
            QPixmap("assets/manual.png").scaled(
                    200, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        manual_img.setAlignment(Qt.AlignCenter)

        self.btn_download = QPushButton("BAIXAR")
        self.btn_download.setFixedSize(160, 45)
        self.btn_download.setCursor(Qt.PointingHandCursor)
        self.btn_download.setStyleSheet("""
                QPushButton {
                    background-color: #3D136F;
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 20px;
                }
                QPushButton:hover {
                    background-color: #5E2A91;
                }
            """)

        right_col.addWidget(text_right)
        right_col.addSpacing(10)
        right_col.addWidget(manual_title)
        right_col.addWidget(manual_img)
        right_col.addWidget(self.btn_download, alignment=Qt.AlignCenter)

        right_col.addSpacing(30)

        qa_title = QLabel("Q&A – PERGUNTAS E RESPOSTAS")
        qa_title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #5B2A86;
        """)

        right_col.addWidget(qa_title)

        # QUESTIONS
        right_col.addWidget(QAItem(
            "Como imprimir ou exportar relatório?",
            "Acesse o menu Relatórios, selecione o período desejado e clique em Exportar."
        ))

        right_col.addWidget(QAItem(
            "Como cadastrar ou editar um funcionário ou produto?",
            "Vá até o menu Cadastros e selecione Funcionários ou Produtos."
        ))

        right_col.addWidget(QAItem(
            "Como solicitar retirada de material?",
            "No menu Almoxarifado, selecione Solicitar Retirada."
        ))

        right_col.addWidget(QAItem(
            "Como eu sei qual permissão eu tenho?",
            "As permissões são exibidas no menu Meu Perfil."
        ))

        # ADD COLUMNS
        content_layout.addLayout(left_col, 2)
        content_layout.addLayout(right_col, 1)

        

 
    # COMPONENTS
    def top_button_style(self):
        return """
                QPushButton {
                    color: white;
                    font-size: 20px;
                    background: transparent;
                    border: none;
                }
                QPushButton:hover {
                    color: #E0C8FF;
                }
            """

    def section_title(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
                font-size: 26px;
                font-weight: bold;
                color: #5B2A86;
            """)
        return label

    def paragraph_text(self, bold_first=False):
        label = QLabel()
        label.setWordWrap(True)

        if bold_first:
            label.setText(
                    "<b>Objetivo:</b> orientar o uso seguro do sistema, "
                    "com foco em registro correto, rastreabilidade e "
                    "boas práticas operacionais."
                )
        else:
            label.setText(
                    "Aqui você encontra instruções claras para cada tela, "
                    "regras de acesso, e dicas para evitar erros comuns."
                )

        label.setStyleSheet("""
                font-size: 20px;
                color: #4A2A6A;
            """)
        return label
