from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton


class TopLeftWidget(QWidget):
    # 自定义信号
    home_button_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.home_button = QPushButton("ACE联盟管理系统")
        self.home_button.setObjectName("home_button")

        top_left_layout = QHBoxLayout()
        top_left_layout.addWidget(self.home_button)

        self.setLayout(top_left_layout)

        # 连接按钮点击事件到自定义信号
        self.home_button.clicked.connect(self.emit_home_button_clicked)

    def emit_home_button_clicked(self):
        """发射自定义信号"""

        self.home_button_clicked.emit()
