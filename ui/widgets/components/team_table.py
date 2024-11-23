from PyQt6.QtWidgets import QTableView, QStyledItemDelegate
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt6.QtCore import QRect


class HyperlinkDelegate(QStyledItemDelegate):
    """
    自定义委托，用于显示可点击的超链接文本。
    """
    def paint(self, painter: QPainter, option, index: QModelIndex):
        text = index.data(Qt.ItemDataRole.DisplayRole)
        painter.save()
        painter.setPen(Qt.GlobalColor.blue)  # 设置文本颜色为蓝色
        # 设置下划线
        font = painter.font()
        font.setUnderline(True)
        painter.setFont(font)
        painter.drawText(option.rect, Qt.AlignmentFlag.AlignCenter, text)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if event.type() == event.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton:
                # 发送自定义的信号，或直接调用模型的方法
                model.handle_hyperlink_click(index)
                return True
        return False


class TeamTableModel(QAbstractTableModel):
    """
    自定义的队伍表格模型，继承自 QAbstractTableModel。
    """
    # 定义列索引
    COLUMN_TEAM_NAME = 0
    COLUMN_CAPTAIN = 1
    COLUMN_COMPOSITION = 2
    COLUMN_FORMATION_DATE = 3
    COLUMN_POINTS = 4
    COLUMN_LEVEL = 5

    def __init__(self, team_service=None):
        super().__init__()
        self.teams = []
        self.team_service = team_service  # 引用业务逻辑层的服务类

    def set_teams(self, teams):
        """
        设置队伍数据并刷新模型。
        """
        self.beginResetModel()
        self.teams = teams if teams is not None else []
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.teams)

    def columnCount(self, parent=QModelIndex()):
        return 6  # 六列

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.teams)):
            return None

        team = self.teams[index.row()]
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if column == self.COLUMN_TEAM_NAME:
                return team.TeamName
            elif column == self.COLUMN_CAPTAIN:
                # return team.captain.PlayerName if team.captain else "未指定"
                return team.TeamName
            elif column == self.COLUMN_COMPOSITION:
                return "查看队伍配置"
            elif column == self.COLUMN_FORMATION_DATE:
                # return team.FormationDate.strftime("%Y-%m-%d") if team.FormationDate else "未知"
                return team.TeamName
            elif column == self.COLUMN_POINTS:
                # return str(team.Points)
                return team.TeamName
            elif column == self.COLUMN_LEVEL:
                # return team.Level or "未知"
                return team.TeamName
        elif role == Qt.ItemDataRole.EditRole:
            if column == self.COLUMN_TEAM_NAME:
                return team.TeamName
        elif role == Qt.ItemDataRole.ForegroundRole:
            if column in (self.COLUMN_CAPTAIN, self.COLUMN_COMPOSITION, self.COLUMN_POINTS):
                return Qt.GlobalColor.blue  # 设置超链接颜色
        elif role == Qt.ItemDataRole.FontRole:
            if column in (self.COLUMN_CAPTAIN, self.COLUMN_COMPOSITION, self.COLUMN_POINTS):
                font = QPainter().font()
                font.setUnderline(True)  # 添加下划线
                return font
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                headers = ["队伍名称", "队长", "队伍配置", "建队日期", "队伍积分", "等级"]
                if 0 <= section < len(headers):
                    return headers[section]
        return None

    def flags(self, index):
        """
        返回指定索引的项标志。
        """
        base_flags = super().flags(index)
        if not index.isValid():
            return base_flags

        column = index.column()
        if column == self.COLUMN_TEAM_NAME:
            return base_flags | Qt.ItemFlag.ItemIsEditable  # 允许编辑
        else:
            return base_flags

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        """
        设置指定索引的数据。
        """
        if not index.isValid():
            return False

        if role == Qt.ItemDataRole.EditRole:
            team = self.teams[index.row()]
            column = index.column()
            if column == self.COLUMN_TEAM_NAME:
                old_name = team.TeamName
                team.TeamName = value
                # 在这里调用业务逻辑层更新数据库中的队伍名称
                if self.team_service:
                    try:
                        self.team_service.update_team(team.TeamID, value)
                        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])
                        return True
                    except ValueError as e:
                        team.TeamName = old_name  # 恢复原名称
                        # 可以在这里显示错误信息
                        print(f"更新队伍名称失败：{e}")
                        return False
        return False

    def handle_hyperlink_click(self, index):
        """
        处理超链接点击事件。
        """
        column = index.column()
        team = self.get_team_at_index(index.row())
        if column == self.COLUMN_CAPTAIN:
            # 处理队长的点击事件
            print(f"点击了队长：{team.captain.PlayerName if team.captain else '未指定'}")
            # 在这里可以打开队长的详细信息窗口
        elif column == self.COLUMN_COMPOSITION:
            # 处理队伍配置的点击事件
            print(f"点击了队伍配置：{team.TeamName}")
            # 在这里可以打开队伍配置窗口
        elif column == self.COLUMN_POINTS:
            # 处理队伍积分的点击事件
            print(f"点击了队伍积分：{team.Points}")
            # 在这里可以打开积分详情窗口

    def get_team_at_index(self, row):
        """
        获取指定行的队伍对象。
        """
        if 0 <= row < len(self.teams):
            return self.teams[row]
        return None


class TeamTable(QTableView):
    """
    自定义的队伍表格视图，继承自 QTableView。
    """
    def __init__(self, team_service=None):
        super().__init__()
        self.model = TeamTableModel(team_service)
        self.setModel(self.model)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)  # 设置为整行选择
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)    # 设置为单选模式
        self.verticalHeader().setVisible(False)                            # 隐藏垂直表头
        self.horizontalHeader().setStretchLastSection(True)                # 最后一列自动拉伸填充

        # 设置自定义委托
        hyperlink_delegate = HyperlinkDelegate(self)
        self.setItemDelegateForColumn(self.model.COLUMN_CAPTAIN, hyperlink_delegate)
        self.setItemDelegateForColumn(self.model.COLUMN_COMPOSITION, hyperlink_delegate)
        self.setItemDelegateForColumn(self.model.COLUMN_POINTS, hyperlink_delegate)

    def set_teams(self, teams):
        """
        设置队伍数据。
        """
        self.model.set_teams(teams)

    def get_selected_team(self):
        """
        获取当前选中的队伍。
        """
        index = self.currentIndex()
        if index.isValid():
            return self.model.get_team_at_index(index.row())
        return None
