from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QMessageBox
from ui.widgets.components.team_table import TeamTable
from ui.widgets.dialogs.add_team_dialog import AddTeamDialog


class TeamManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 工具栏
        toolbar_layout = QHBoxLayout()
        self.add_button = QPushButton("添加队伍")
        self.edit_button = QPushButton("修改队伍")
        self.delete_button = QPushButton("删除队伍")
        self.refresh_button = QPushButton("刷新列表")

        toolbar_layout.addWidget(self.add_button)
        toolbar_layout.addWidget(self.edit_button)
        toolbar_layout.addWidget(self.delete_button)
        toolbar_layout.addWidget(self.refresh_button)
        toolbar_layout.addStretch()

        # 队伍列表
        self.team_table = TeamTable()
        self.load_teams()

        # 连接信号和槽
        self.add_button.clicked.connect(self.add_team)
        self.edit_button.clicked.connect(self.edit_team)
        self.delete_button.clicked.connect(self.delete_team)
        self.refresh_button.clicked.connect(self.load_teams)

        # 布局设置
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.team_table)
        self.setLayout(layout)

    def load_teams(self):
        # 从服务层获取队伍数据，加载到表格中
        teams = self.get_all_teams()
        self.team_table.set_teams(teams)

    def add_team(self):
        dialog = AddTeamDialog()
        if dialog.exec():
            team_name = dialog.get_team_name()
            if team_name:
                self.add_team_to_db(team_name)
                self.load_teams()

    def edit_team(self):
        selected_team = self.team_table.get_selected_team()
        if not selected_team:
            QMessageBox.warning(self, "提示", "请先选择要修改的队伍。")
            return
        dialog = AddTeamDialog(selected_team.TeamName)
        if dialog.exec():
            new_name = dialog.get_team_name()
            if new_name:
                self.update_team_in_db(selected_team.TeamID, new_name)
                self.load_teams()

    def delete_team(self):
        selected_team = self.team_table.get_selected_team()
        if not selected_team:
            QMessageBox.warning(self, "提示", "请先选择要删除的队伍。")
            return
        reply = QMessageBox.question(self, "确认", f"确定要删除队伍 '{selected_team.TeamName}' 吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_team_from_db(selected_team.TeamID)
            self.load_teams()

    # 以下方法需要调用服务层的接口，与数据库交互
    def get_all_teams(self):
        # 调用 TeamService.get_all_teams()
        pass

    def add_team_to_db(self, team_name):
        # 调用 TeamService.add_team(team_name)
        pass

    def update_team_in_db(self, team_id, new_name):
        # 调用 TeamService.update_team(team_id, new_name)
        pass

    def delete_team_from_db(self, team_id):
        # 调用 TeamService.delete_team(team_id)
        pass
