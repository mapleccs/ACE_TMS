from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class PlayerManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("玩家管理")
        layout = QVBoxLayout()
        label = QLabel("这是玩家管理界面")
        layout.addWidget(label)
        self.setLayout(layout)
