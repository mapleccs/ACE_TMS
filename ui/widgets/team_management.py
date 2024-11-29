from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ui.widgets.components.team_table import TeamTableView, TeamTableModel


class TeamManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 初始化TeamTable视图，显示队伍信息
        self.team_table = TeamTableView()  # 使用TeamTable来显示数据
        layout.addWidget(self.team_table)

        # 模拟数据
        self.teams = [
            {'队伍名称': 'Team A', '队长ID': 'Player 1', '联系方式': '10086', '队伍配置': '10人',
             '建队日期': '2024-10-10', '队伍积分': 10, '队伍等级': 'C'},
            {'队伍名称': 'Team B', '队长ID': 'Player 2', '联系方式': '10087', '队伍配置': '12人',
             '建队日期': '2024-10-12', '队伍积分': 6, '队伍等级': 'D'},
            {'队伍名称': 'Team C', '队长ID': 'Player 3', '联系方式': '10088', '队伍配置': '15人',
             '建队日期': '2024-10-14', '队伍积分': 12, '队伍等级': 'C'},
        ]

        self.model = TeamTableModel(self.teams)

        # 将模拟数据传递给TeamTable
        self.team_table.setModel(self.model)

        # 设置布局
        self.setLayout(layout)

    def update_table_data(self, search_text):
        """根据搜索文本更新表格数据"""
        filtered_data = self.filter_teams(search_text)
        self.model.set_data(filtered_data)
        self.team_table.reset()

    def filter_teams(self, search_text):
        """根据搜索文本过滤队伍数据"""
        filtered_data = []
        for team in self.model._data:
            if search_text.lower() in team['队伍名称'].lower():
                filtered_data.append(team)
        return filtered_data
