from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class TeamHonorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setObjectName("team_honor_layout")
        layout.addWidget(QPushButton("荣誉按钮"))
        # 添加更多荣誉相关的控件
