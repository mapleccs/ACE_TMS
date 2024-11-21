# ui/widgets/team_management.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from services.team_service import TeamService
from utils.db_utils import get_database_session
from PyQt6.QtCore import Qt
from ui.widgets.dialogs.add_team_dialog import AddTeamDialog


class TeamManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        session = get_database_session()
        self.team_service = TeamService(session)
        self.init_ui()
        self.load_teams()

    def init_ui(self):
        layout = QVBoxLayout()

        # 按钮布局
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加队伍")
        self.edit_button = QPushButton("修改队伍")
        self.delete_button = QPushButton("删除队伍")

        # 连接按钮事件
        self.add_button.clicked.connect(self.add_team)
        self.edit_button.clicked.connect(self.edit_team)
        self.delete_button.clicked.connect(self.delete_team)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        # 表格
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(1)
        self.table_widget.setHorizontalHeaderLabels(["队伍名称"])
        self.table_widget.setSelectionBehavior(self.table_widget.SelectionBehavior.SelectRows)
        self.table_widget.setSelectionMode(self.table_widget.SelectionMode.SingleSelection)

        layout.addLayout(button_layout)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def load_teams(self):
        teams = self.team_service.get_all_teams()
        self.table_widget.setRowCount(len(teams))
        for row, team in enumerate(teams):
            self.table_widget.setItem(row, 0, QTableWidgetItem(team.TeamName))
            self.table_widget.item(row, 0).setData(Qt.ItemDataRole.UserRole, team.TeamID)

    def add_team(self):
        dialog = AddTeamDialog()
        if dialog.exec():
            team_name = dialog.team_name_input.text()
            if team_name:
                try:
                    self.team_service.add_team(team_name)
                    self.load_teams()
                    QMessageBox.information(self, "成功", "队伍添加成功！")
                except ValueError as e:
                    QMessageBox.warning(self, "错误", str(e))

    def edit_team(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择要修改的队伍。")
            return
        team_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        team = self.team_service.get_team_by_id(team_id)
        if team:
            dialog = AddTeamDialog(team.TeamName)
            if dialog.exec():
                new_name = dialog.team_name_input.text()
                if new_name:
                    try:
                        self.team_service.update_team(team_id, new_name)
                        self.load_teams()
                        QMessageBox.information(self, "成功", "队伍修改成功！")
                    except ValueError as e:
                        QMessageBox.warning(self, "错误", str(e))

    def delete_team(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择要删除的队伍。")
            return
        team_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(self, '确认', '确定要删除选中的队伍吗？',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.team_service.delete_team(team_id)
                self.load_teams()
                QMessageBox.information(self, "成功", "队伍删除成功！")
            except ValueError as e:
                QMessageBox.warning(self, "错误", str(e))
