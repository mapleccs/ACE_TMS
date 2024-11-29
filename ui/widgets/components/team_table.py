from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt6.QtWidgets import QTableView, QMessageBox, QHeaderView


# 模型
class TeamTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data = []
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 7  # 7列

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None
        row = index.row()
        column = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            headers = ['队伍名称', '队长ID', '联系方式', '队伍配置', '建队日期', '队伍积分', '队伍等级']
            return self._data[row][headers[column]]
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.ItemDataRole.DisplayRole:
            headers = ['队伍名称', '队长ID', '联系方式', '队伍配置', '建队日期', '队伍积分', '队伍等级']
            return QVariant(headers[section])
        return None


# 视图
class TeamTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectItems)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        # 隐藏行号
        self.verticalHeader().setVisible(False)  # 隐藏垂直表头（行号）

        # 设置每列宽度均匀分配
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # 均匀填充宽度

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            if index.column() == 3:  # "队伍配置"列是第3列（列索引3）
                self.on_config_cell_click(index)
        super().mousePressEvent(event)

    def on_config_cell_click(self, index: QModelIndex):
        config_value = self.model().data(index, Qt.ItemDataRole.DisplayRole)
        self.show_config_info(config_value)

    def show_config_info(self, config_value):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("队伍配置详情")
        msg.setText(f"队伍配置值为：{config_value}")
        msg.exec()
