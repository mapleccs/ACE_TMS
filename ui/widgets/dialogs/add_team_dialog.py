from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout


class AddTeamDialog(QDialog):
    def __init__(self, team_name=''):
        super().__init__()
        self.setWindowTitle("添加队伍" if not team_name else "修改队伍")
        self.team_name_input = QLineEdit()
        self.team_name_input.setText(team_name)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("队伍名称："))
        layout.addWidget(self.team_name_input)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
