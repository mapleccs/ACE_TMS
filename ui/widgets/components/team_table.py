from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSignal
from PyQt6.QtWidgets import QTableView, QHeaderView


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

    def set_data(self, data):
        """更新数据并刷新表格"""
        self.beginResetModel()  # 开始重置模型，通知视图更新
        self._data = data
        self.endResetModel()  # 结束重置模型


# 视图
class TeamTableView(QTableView):
    team_selected = pyqtSignal(str)

    def __init__(self, stacked_widget=None, parent=None):
        super().__init__(parent)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectItems)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        # 隐藏行号
        self.verticalHeader().setVisible(False)

        # 设置每列宽度均匀分配
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.stacked_widget = stacked_widget  # 将 stacked_widget 传递给视图，用于页面切换

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            print(f"点击了 {index.row()} 行，{index.column()} 列")  # 打印行和列
            if index.column() == 3:  # "队伍配置"列是第3列（列索引3）
                team_name = self.model().data(self.model().index(index.row(), 0), Qt.ItemDataRole.DisplayRole)
                print(f"选中的队伍名称是：{team_name}")  # 打印选中的队伍名称
                self.team_selected.emit(team_name)  # 发出队伍名称信号
            else:
                print("点击的不是'队伍配置'列")
        super().mousePressEvent(event)
