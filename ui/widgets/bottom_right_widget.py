from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from ui.widgets.team_management import TeamManagementWidget
from ui.widgets.match_management import MatchManagementWidget
from ui.widgets.player_management import PlayerManagementWidget
from ui.widgets.team_detail_data_widget import TeamDetailDataWidget


class BottomRightWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.right_panel = QStackedWidget()

        self.home_page_label = QLabel("欢迎使用ACE联盟数据管理系统")
        self.home_page_label.setObjectName("home_page_label")
        self.home_page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.team_management_widget = TeamManagementWidget()
        self.team_detail_data_widget = TeamDetailDataWidget()
        self.match_management_widget = MatchManagementWidget()
        self.player_management_widget = PlayerManagementWidget()

        self.right_panel.addWidget(self.home_page_label)
        self.right_panel.addWidget(self.team_management_widget)
        self.right_panel.addWidget(self.team_detail_data_widget)
        self.right_panel.addWidget(self.match_management_widget)
        self.right_panel.addWidget(self.player_management_widget)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.right_panel)

        # 默认显示战队数据界面
        self.right_panel.setCurrentWidget(self.home_page_label)
