from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from ui.widgets.team_management import TeamManagementWidget
from ui.widgets.match_management import MatchManagementWidget
from ui.widgets.player_management import PlayerManagementWidget
from ui.widgets.team_detail_data_widget import TeamDetailDataWidget


class BottomRightWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("bottom_right_widget")  # 设置主控件名称

        self.right_panel = QStackedWidget()
        self.right_panel.setObjectName('right_panel')  # 设置右侧面板名称

        self.home_page_label = QLabel("欢迎使用ACE联盟数据管理系统")
        self.home_page_label.setObjectName("home_page_label")  # 设置首页标签名称
        self.home_page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.team_management_widget = TeamManagementWidget()
        self.team_management_widget.setObjectName('team_management_widget')  # 设置战队管理页面名称

        self.team_detail_data_widget = TeamDetailDataWidget()
        self.team_detail_data_widget.setObjectName('team_detail_data_widget')  # 设置战队数据详情页面名称

        self.match_management_widget = MatchManagementWidget()
        self.match_management_widget.setObjectName('match_management_widget')  # 设置比赛管理页面名称

        self.player_management_widget = PlayerManagementWidget()
        self.player_management_widget.setObjectName('player_management_widget')  # 设置球员管理页面名称

        self.right_panel.addWidget(self.home_page_label)
        self.right_panel.addWidget(self.team_management_widget)
        self.right_panel.addWidget(self.team_detail_data_widget)
        self.right_panel.addWidget(self.match_management_widget)
        self.right_panel.addWidget(self.player_management_widget)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.right_panel)

        # 默认显示战队数据界面
        self.right_panel.setCurrentWidget(self.home_page_label)
