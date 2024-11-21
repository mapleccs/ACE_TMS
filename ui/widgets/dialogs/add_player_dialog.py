from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout


class AddPlayerDialog(QDialog):
    def __init__(self, player_name=''):
        super().__init__()
        self.setWindowTitle("添加玩家" if not player_name else "修改玩家")
        self.player_name_input = QLineEdit()
        self.player_name_input.setText(player_name)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("玩家名称："))
        layout.addWidget(self.player_name_input)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
