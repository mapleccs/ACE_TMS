from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFormLayout


class AddPlayerDialog(QDialog):
    def __init__(self, player_name='', in_game_name='', preferred_roles=''):
        super().__init__()
        self.setWindowTitle("添加玩家" if not player_name else "修改玩家")
        self.player_name_input = QLineEdit()
        self.player_name_input.setText(player_name)
        self.in_game_name_input = QLineEdit()
        self.in_game_name_input.setText(in_game_name)
        self.preferred_roles_input = QLineEdit()
        self.preferred_roles_input.setText(preferred_roles)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.addRow("玩家姓名：", self.player_name_input)
        form_layout.addRow("游戏昵称：", self.in_game_name_input)
        form_layout.addRow("偏好位置：", self.preferred_roles_input)
        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
