from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from services.player_service import PlayerService
from utils.db_utils import get_database_session
from PyQt6.QtCore import Qt
from ui.widgets.dialogs.add_player_dialog import AddPlayerDialog


class PlayerManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        session = get_database_session()
        self.player_service = PlayerService(session)
        self.init_ui()
        self.load_players()

    def init_ui(self):
        layout = QVBoxLayout()

        # 按钮布局
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加玩家")
        self.edit_button = QPushButton("修改玩家")
        self.delete_button = QPushButton("删除玩家")

        # 连接按钮事件
        self.add_button.clicked.connect(self.add_player)
        self.edit_button.clicked.connect(self.edit_player)
        self.delete_button.clicked.connect(self.delete_player)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        # 表格
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["玩家姓名", "游戏昵称", "偏好位置"])
        self.table_widget.setSelectionBehavior(self.table_widget.SelectionBehavior.SelectRows)
        self.table_widget.setSelectionMode(self.table_widget.SelectionMode.SingleSelection)

        layout.addLayout(button_layout)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def load_players(self):
        players = self.player_service.get_all_players()
        self.table_widget.setRowCount(len(players))
        for row, player in enumerate(players):
            self.table_widget.setItem(row, 0, QTableWidgetItem(player.PlayerName))
            self.table_widget.setItem(row, 1, QTableWidgetItem(player.InGameName or ""))
            self.table_widget.setItem(row, 2, QTableWidgetItem(player.PreferredRoles or ""))
            self.table_widget.item(row, 0).setData(Qt.ItemDataRole.UserRole, player.PlayerID)

    def add_player(self):
        dialog = AddPlayerDialog()
        if dialog.exec():
            player_name = dialog.player_name_input.text()
            in_game_name = dialog.in_game_name_input.text()
            preferred_roles = dialog.preferred_roles_input.text()
            if player_name:
                try:
                    self.player_service.add_player(player_name, in_game_name, preferred_roles)
                    self.load_players()
                    QMessageBox.information(self, "成功", "玩家添加成功！")
                except ValueError as e:
                    QMessageBox.warning(self, "错误", str(e))

    def edit_player(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择要修改的玩家。")
            return
        player_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        player = self.player_service.get_player_by_id(player_id)
        if player:
            dialog = AddPlayerDialog(player.PlayerName, player.InGameName, player.PreferredRoles)
            if dialog.exec():
                new_name = dialog.player_name_input.text()
                in_game_name = dialog.in_game_name_input.text()
                preferred_roles = dialog.preferred_roles_input.text()
                try:
                    self.player_service.update_player(player_id, new_name, in_game_name, preferred_roles)
                    self.load_players()
                    QMessageBox.information(self, "成功", "玩家修改成功！")
                except ValueError as e:
                    QMessageBox.warning(self, "错误", str(e))

    def delete_player(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择要删除的玩家。")
            return
        player_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(self, '确认', '确定要删除选中的玩家吗？',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.player_service.delete_player(player_id)
                self.load_players()
                QMessageBox.information(self, "成功", "玩家删除成功！")
            except ValueError as e:
                QMessageBox.warning(self, "错误", str(e))
