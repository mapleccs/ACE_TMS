from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class MatchManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("比赛管理")
        layout = QVBoxLayout()
        label = QLabel("这是比赛管理界面")
        layout.addWidget(label)
        self.setLayout(layout)
