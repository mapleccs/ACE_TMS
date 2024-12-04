import re
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ui.widgets.components.team_table import TeamTableView, TeamTableModel
from services.team_service import TeamService
from utils.db_utils import get_database_session


class TeamManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 初始化TeamTable视图，显示队伍信息
        self.team_table = TeamTableView()
        layout.addWidget(self.team_table)

        # 获取服务层返回的teams数据
        session = get_database_session()
        team_service = TeamService(session)
        self.teams = team_service.get_all_teams()

        self.model = TeamTableModel(self.teams)

        # 将数据传递给TeamTable
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
