from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from services.team_service import TeamService
from utils.db_utils import get_database_session
from ui.widgets.components.team_table import TeamTable


class TeamManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        session = get_database_session()
        self.team_service = TeamService(session)
        self.init_ui()
        self.load_teams()

    def init_ui(self):
        layout = QVBoxLayout()

        # 按钮布局
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加队伍")
        self.edit_button = QPushButton("修改队伍")
        self.delete_button = QPushButton("删除队伍")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        self.team_table = TeamTable(self.team_service)
        layout.addLayout(button_layout)
        layout.addWidget(self.team_table)
        self.setLayout(layout)

    def load_teams(self):
        teams = self.team_service.get_all_teams()
        self.team_table.set_teams(teams)
