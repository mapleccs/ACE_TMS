from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal


class TeamPlayerRegistrationWidget(QWidget):
    # 定义一个自定义信号，当点击“返回”按钮时发射
    back_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # 示例控件
        label = QLabel("队员登记面板", self)
        layout.addWidget(label)

        # 添加“返回”按钮
        self.back_button = QPushButton("返回", self)
        self.back_button.setObjectName("team_button")
        layout.addWidget(self.back_button)

        # 连接“返回”按钮的点击信号到自定义信号
        self.back_button.clicked.connect(self.back_clicked.emit)
