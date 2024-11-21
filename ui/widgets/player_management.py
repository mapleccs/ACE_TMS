from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from ui.widgets.dialogs.add_player_dialog import AddPlayerDialog


class PlayerManagementWidget(QWidget):
    def __init__(self, player_service):
        super().__init__()
        self.player_service = player_service
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
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["玩家ID", "玩家名称"])
        self.table_widget.setSelectionBehavior(self.table_widget.SelectionBehavior.SelectRows)
        self.table_widget.setSelectionMode(self.table_widget.SelectionMode.SingleSelection)
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        layout.addLayout(button_layout)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def load_players(self):
        players = self.player_service.get_all_players()
        self.table_widget.setRowCount(len(players))
        for row, player in enumerate(players):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(player.PlayerID)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(player.PlayerName))

    def add_player(self):
        dialog = AddPlayerDialog()
        if dialog.exec():
            player_name = dialog.player_name_input.text()
            if player_name:
                try:
                    self.player_service.add_player(player_name)
                    self.load_players()
                except ValueError as e:
                    QMessageBox.warning(self, "错误", str(e))

    def edit_player(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择要修改的玩家。")
            return
        player_id = int(selected_items[0].text())
        player = self.player_service.get_player_by_id(player_id)
        if player:
            dialog = AddPlayerDialog(player.PlayerName)
            if dialog.exec():
                new_name = dialog.player_name_input.text()
                try:
                    self.player_service.update_player(player_id, new_name)
                    self.load_players()
                except ValueError as e:
                    QMessageBox.warning(self, "错误", str(e))

    def delete_player(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择要删除的玩家。")
            return
        reply = QMessageBox.question(self, '确认', '确定要删除选中的玩家吗？',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            player_id = int(selected_items[0].text())
            try:
                self.player_service.delete_player(player_id)
                self.load_players()
            except Exception as e:
                QMessageBox.warning(self, "错误", str(e))
