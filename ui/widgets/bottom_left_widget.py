from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QButtonGroup
from PyQt6.QtGui import QIcon


class BottomLeftWidget(QWidget):
    # 自定义信号
    team_button_clicked = pyqtSignal()
    team_details_entry_button_clicked = pyqtSignal()
    team_details_management_button_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        left_bottom_layout = QVBoxLayout()

        # 创建按钮
        self.team_button = QPushButton("战队数据")
        self.team_button.setIcon(QIcon(r"ui\resources\ICON\信号格.png"))
        self.team_button.setObjectName("left_button")

        self.team_details_entry_button = QPushButton("战队资料录入")
        self.team_details_entry_button.setCheckable(True)  # 设置按钮为可选中状态
        self.team_details_entry_button.setChecked(False)  # 初始为未选中状态
        self.team_details_entry_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.team_details_entry_button.setObjectName("second_button")

        self.team_details_management_button = QPushButton("战队资料管理")
        self.team_details_management_button.setCheckable(True)  # 设置按钮为可选中状态
        self.team_details_management_button.setChecked(False)  # 初始为未选中状态
        self.team_details_management_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.team_details_management_button.setObjectName("second_button")

        self.match_button = QPushButton("对局资料")
        self.match_button.setObjectName("left_button")
        self.match_button.setIcon(QIcon(r"ui\resources\ICON\信号格.png"))

        self.match_details_entry_button = QPushButton("对局资料录入")
        self.match_details_entry_button.setCheckable(True)  # 设置按钮为可选中状态
        self.match_details_entry_button.setChecked(False)  # 初始为未选中状态
        self.match_details_entry_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.match_details_entry_button.setObjectName("second_button")

        self.season_info_stats_button = QPushButton("赛季信息统计")
        self.season_info_stats_button.setCheckable(True)  # 设置按钮为可选中状态
        self.season_info_stats_button.setChecked(False)  # 初始为未选中状态
        self.season_info_stats_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.season_info_stats_button.setObjectName("second_button")

        self.season_info_button = QPushButton("赛季信息")
        self.season_info_button.setObjectName("left_button")
        self.season_info_button.setIcon(QIcon(r"ui\resources\ICON\信号格.png"))

        self.team_match_stats_button = QPushButton("战队比赛统计")
        self.team_match_stats_button.setCheckable(True)  # 设置按钮为可选中状态
        self.team_match_stats_button.setChecked(False)  # 初始为未选中状态
        self.team_match_stats_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.team_match_stats_button.setObjectName("second_button")

        self.player_match_stats_button = QPushButton("选手比赛统计")
        self.player_match_stats_button.setCheckable(True)  # 设置按钮为可选中状态
        self.player_match_stats_button.setChecked(False)  # 初始为未选中状态
        self.player_match_stats_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.player_match_stats_button.setObjectName("second_button")

        self.hero_usage_stats_button = QPushButton("英雄使用统计")
        self.hero_usage_stats_button.setCheckable(True)  # 设置按钮为可选中状态
        self.hero_usage_stats_button.setChecked(False)  # 初始为未选中状态
        self.hero_usage_stats_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.hero_usage_stats_button.setObjectName("second_button")

        # 创建按钮组并添加到该组
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.team_details_entry_button)
        self.button_group.addButton(self.team_details_management_button)
        self.button_group.addButton(self.match_details_entry_button)
        self.button_group.addButton(self.season_info_stats_button)
        self.button_group.addButton(self.team_match_stats_button)
        self.button_group.addButton(self.player_match_stats_button)
        self.button_group.addButton(self.hero_usage_stats_button)

        left_bottom_layout.addWidget(self.team_button)
        left_bottom_layout.addWidget(self.team_details_entry_button)
        left_bottom_layout.addWidget(self.team_details_management_button)
        left_bottom_layout.addWidget(self.match_button)
        left_bottom_layout.addWidget(self.match_details_entry_button)
        left_bottom_layout.addWidget(self.season_info_stats_button)
        left_bottom_layout.addWidget(self.season_info_button)
        left_bottom_layout.addWidget(self.team_match_stats_button)
        left_bottom_layout.addWidget(self.player_match_stats_button)
        left_bottom_layout.addWidget(self.hero_usage_stats_button)

        self.setLayout(left_bottom_layout)

        # 连接按钮点击事件到自定义信号
        self.team_button.clicked.connect(self.emit_team_button_clicked)
        self.team_details_management_button.clicked.connect(self.emit_team_details_management_button_clicked)
        self.team_details_entry_button.clicked.connect(self.team_details_entry_button_clicked)

    def emit_team_button_clicked(self):
        """发射自定义信号"""
        self.team_button_clicked.emit()

    def emit_team_details_entry_button_clicked(self):
        """发射自定义信号"""
        self.team_details_entry_button_clicked.emit()

    def emit_team_details_management_button_clicked(self):
        self.team_details_management_button_clicked.emit()
