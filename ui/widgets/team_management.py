import re
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ui.widgets.components.team_table import TeamTableView, TeamTableModel


class TeamManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 初始化TeamTable视图，显示队伍信息
        self.team_table = TeamTableView()
        layout.addWidget(self.team_table)

        # 模拟数据
        self.teams = [
            {'队伍名称': 'KT1', '队长ID': 'Player 1', '联系方式': '10086', '队伍配置': '10人',
             '建队日期': '2024-10-10', '队伍积分': 16, '队伍等级': 'C'},
            {'队伍名称': 'CB', '队长ID': 'Player 2', '联系方式': '10087', '队伍配置': '12人',
             '建队日期': '2024-10-12', '队伍积分': 15, '队伍等级': 'D'},
            {'队伍名称': 'SSW', '队长ID': 'Player 3', '联系方式': '10088', '队伍配置': '15人',
             '建队日期': '2024-10-14', '队伍积分': 12, '队伍等级': 'C'},
        ]

        self.model = TeamTableModel(self.teams)

        # 将模拟数据传递给TeamTable
        self.team_table.setModel(self.model)

        # 设置布局
        self.setLayout(layout)

    def update_table_data(self, search_text):
        """根据搜索文本更新表格数据"""
        if not search_text:
            # 如果搜索文本为空，显示所有数据
            self.model.set_data(self.teams)
        else:
            # 根据搜索文本过滤数据
            filtered_data = self.filter_teams(search_text)
            self.model.set_data(filtered_data)  # 更新模型数据
        self.team_table.reset()

    def filter_teams(self, search_text):
        """根据搜索文本过滤队伍数据"""
        filtered_data = []
        for team in self.teams:
            if search_text.lower() in team['队伍名称'].lower():
                filtered_data.append(team)
        return filtered_data

    def sort_teams(self, sort_criteria):
        """根据选择的排序标准对队伍进行排序"""
        if sort_criteria == "排序方式：队名":
            self.teams.sort(key=lambda x: x['队伍名称'])
        elif sort_criteria == "排序方式：人数":
            self.teams.sort(key=self.extract_team_size, reverse=True)
        elif sort_criteria == "排序方式：日期":
            self.teams.sort(key=lambda x: x['建队日期'])
        elif sort_criteria == "排序方式：积分":
            self.teams.sort(key=lambda x: x['队伍积分'], reverse=True)  # 积分越高越好

        # 更新表格数据
        self.model.set_data(self.teams)
        self.team_table.reset()

    def extract_team_size(self, team):
        """从'队伍配置'字段中提取数字部分并返回"""
        match = re.search(r'(\d+)', team['队伍配置'])  # 提取数字部分
        if match:
            return int(match.group(1))  # 返回数字
        return 0  # 如果没有找到数字，返回0
