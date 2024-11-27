from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from ui.widgets.components.team_table import TeamTable


class TeamManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.team_button = QPushButton("战队数据")
        self.team_table = TeamTable()
        layout.addWidget(self.team_button)
        layout.addWidget(self.team_table)
        self.setLayout(layout)

        # 模拟数据
        teams = [
            {'队伍名称': 'Team A', '队长ID': 'Player 1', '联系方式': '10086', '队伍配置': 10, '建队日期': '2024-10-10', '队伍积分': 10, '队伍等级': 'C'},
            {'队伍名称': 'Team B', '队长ID': 'Player 2', '联系方式': '10087', '队伍配置': 12, '建队日期': '2024-10-12', '队伍积分': 6, '队伍等级': 'D'},
            {'队伍名称': 'Team C', '队长ID': 'Player 3', '联系方式': '10088', '队伍配置': 15, '建队日期': '2024-10-14', '队伍积分': 12, '队伍等级': 'C'},
        ]

        # 将模拟数据传递给表格
        self.team_table.set_teams(teams)

