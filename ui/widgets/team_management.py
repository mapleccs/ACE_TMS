# 在界面中
from PyQt6.QtWidgets import QWidget, QVBoxLayout
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
        self.team_table = TeamTable(self.team_service)
        layout.addWidget(self.team_table)
        self.setLayout(layout)

    def load_teams(self):
        teams = self.team_service.get_all_teams()
        self.team_table.set_teams(teams)
