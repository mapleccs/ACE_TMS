from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSignal
from PyQt6.QtWidgets import QTableView, QHeaderView


# 模型
class TeamMembershipTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data = []
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 5  # 根据实际需要调整列数

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None
        row = index.row()
        column = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            headers = ['位置', '昵称', '游戏ID', '积分', '职务']
            return self._data[row][headers[column]]
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.ItemDataRole.DisplayRole:
            headers = ['位置', '昵称', '游戏ID', '积分', '职务']
            if orientation == Qt.Orientation.Horizontal:
                return QVariant(headers[section])
            else:
                return QVariant(section + 1)
        return None

    def set_data(self, data):
        """更新数据并刷新表格"""
        self.beginResetModel()
        self._data = data
        self.endResetModel()


# 视图
class TeamMembershipTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("TeamMembershipTableView")
        # self.setSelectionBehavior(QTableView.SelectionBehavior.SelectItems)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        # 隐藏行号
        self.verticalHeader().setVisible(False)

        # 设置每列宽度均匀分配
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
