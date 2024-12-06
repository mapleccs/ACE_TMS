from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QUrl
from PyQt6.QtGui import QIcon, QBrush, QColor, QDesktopServices
from PyQt6.QtWidgets import QTableView, QHeaderView


# 模型
class MatchRecordsTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data = []
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 6

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None
        row = index.row()
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            headers = ['胜负', '时间', '比分', '赛事类型', '回放', '数据']
            visible_columns = {'胜负', '时间', '比分', '赛事类型'}  # 可见列集合

            header_name = headers[column]
            if header_name in visible_columns:
                return self._data[row][header_name]  # 返回数据
            else:
                return None  # 不显示不需要的列
        elif role == Qt.ItemDataRole.DecorationRole:
            if column == 4:  # “回放”列
                return QIcon('ui/resources/ICON/播放.png')  # 替换为你的回放图标路径rn None
            if column == 5:  # "数据"列
                return QIcon('ui/resources/ICON/对局数据.png')
        elif role == Qt.ItemDataRole.BackgroundRole:
            if self._data[row]['胜负'] == 'WIN':
                return QBrush(QColor(144, 238, 144))  # 绿色背景
            elif self._data[row]['胜负'] == 'LOSE':
                return QBrush(QColor(255, 160, 122))  # 红色背景
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.ItemDataRole.DisplayRole:
            headers = ['胜负', '时间', '比分', '赛事类型', '回放', '数据']
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
class MatchRecordsTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置对象名称（用于在 QSS 中进行定制）
        self.setObjectName("match_records_table_view")

        # self.setSelectionBehavior(QTableView.SelectionBehavior.SelectItems)
        # self.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        # 隐藏行号
        self.verticalHeader().setVisible(False)

        # 设置每列宽度均匀分配
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            if index.column() == 4:  # 点击“回放”列（第5列，索引4）
                playback_link = self.model().data(self.model().index(index.row(), 4), Qt.ItemDataRole.DisplayRole)
                if playback_link:
                    QDesktopServices.openUrl(QUrl(playback_link))
                else:
                    # 如果没有指定链接，默认跳转到 Bilibili
                    QDesktopServices.openUrl(QUrl("https://www.bilibili.com"))
        super().mousePressEvent(event)

