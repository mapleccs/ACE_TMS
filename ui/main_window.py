from PyQt6.QtWidgets import QMainWindow, QTabWidget
from ui.widgets.team_management import TeamManagementWidget
from ui.widgets.player_management import PlayerManagementWidget
from ui.widgets.match_management import MatchManagementWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("ACE联盟比赛管理系统")
        self.resize(1000, 600)
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget(parent=self)
        self.tabs.addTab(TeamManagementWidget(), "队伍管理")
        self.tabs.addTab(PlayerManagementWidget(), "玩家管理")
        # self.tabs.addTab(MatchManagementWidget(), "比赛管理")
        self.setCentralWidget(self.tabs)
