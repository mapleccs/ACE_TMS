from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QRect
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QTableView, QStyledItemDelegate, QVBoxLayout, QPushButton


class HyperlinkDelegate(QStyledItemDelegate):
    """
    自定义委托，用于显示可点击的超链接文本。
    """

    def paint(self, painter, option, index):
        text = index.data(Qt.ItemDataRole.DisplayRole)
        if text:
            painter.save()
            painter.setPen(QColor(0, 0, 255))  # 设置文本颜色为蓝色
            font = painter.font()
            font.setUnderline(True)  # 设置下划线
            painter.setFont(font)
            painter.drawText(option.rect, Qt.AlignmentFlag.AlignCenter, text)
            painter.restore()

    def editorEvent(self, event, model, option, index):
        """
        处理超链接点击事件。
        """
        if event.type() == event.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton:
                model.handle_hyperlink_click(index)
                return True
        return False


class ButtonDelegate(QStyledItemDelegate):
    """
    自定义委托，用于在单元格内显示按钮。
    """

    def paint(self, painter, option, index):
        text = index.data(Qt.ItemDataRole.DisplayRole)
        if text:
            button_rect = QRect(option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height())
            painter.save()
            painter.setBrush(Qt.GlobalColor.lightGray)  # 按钮背景颜色
            painter.drawRect(button_rect)
            painter.setPen(Qt.GlobalColor.black)  # 按钮文字颜色
            painter.drawText(button_rect, Qt.AlignmentFlag.AlignCenter, text)
            painter.restore()

    def editorEvent(self, event, model, option, index):
        """
        处理按钮点击事件。
        """
        if event.type() == event.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton:
                model.handle_button_click(index)
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

    def fetch_teams(self):
        """
        获取所有队伍数据并更新表格。
        """
        if self.team_service:
            teams = self.team_service.get_all_teams()  # 获取所有队伍
            self.set_teams(teams)  # 设置队伍数据并刷新表格

    def rowCount(self, parent=QModelIndex()):
        return len(self.teams)

    def columnCount(self, parent=QModelIndex()):
        return 6  # 六列

    def get_column_data(self, team, column):
        """
        根据列索引返回对应的数据。避免重复代码。
        """
        data_map = {
            self.COLUMN_TEAM_NAME: team.TeamName,
            self.COLUMN_CAPTAIN: team.TeamName,  # 可以更改为队长信息
            self.COLUMN_COMPOSITION: "查看队伍配置",
            self.COLUMN_FORMATION_DATE: team.TeamName,  # 可根据需要更改为建队日期
            self.COLUMN_POINTS: team.TeamName,  # 可根据需要更改为积分
            self.COLUMN_LEVEL: team.TeamName,  # 可根据需要更改为等级
        }
        return data_map.get(column, None)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.teams)):
            return None

        team = self.teams[index.row()]
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            return self.get_column_data(team, column)

        if role == Qt.ItemDataRole.ForegroundRole:
            # 设置超链接颜色
            if column in [self.COLUMN_CAPTAIN, self.COLUMN_COMPOSITION, self.COLUMN_POINTS]:
                return Qt.GlobalColor.blue

        if role == Qt.ItemDataRole.FontRole:
            # 为超链接列设置下划线
            if column in [self.COLUMN_CAPTAIN, self.COLUMN_COMPOSITION, self.COLUMN_POINTS]:
                font = QPainter().font()
                font.setUnderline(True)
                return font

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                headers = ["队伍名称", "队长", "队伍配置", "建队日期", "队伍积分", "等级"]
                return headers[section] if 0 <= section < len(headers) else None
        return None

    def flags(self, index):
        """
        返回指定索引的项标志。
        """
        base_flags = super().flags(index)
        if not index.isValid():
            return base_flags

        column = index.column()
        # 允许编辑队伍名称列
        if column == self.COLUMN_TEAM_NAME:
            return base_flags | Qt.ItemFlag.ItemIsEditable
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
                # 更新数据库中的队伍名称
                if self.team_service:
                    try:
                        self.team_service.update_team(team.TeamID, value)
                        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])
                        return True
                    except ValueError as e:
                        team.TeamName = old_name  # 恢复原名称
                        print(f"更新队伍名称失败：{e}")
                        return False
        return False

    def handle_hyperlink_click(self, index):
        """
        处理超链接点击事件。
        """
        team = self.get_team_at_index(index.row())
        column = index.column()
        if column == self.COLUMN_CAPTAIN:
            print(f"点击了队长：{team.TeamName}")
        elif column == self.COLUMN_COMPOSITION:
            print(f"点击了队伍配置：{team.TeamName}")
        elif column == self.COLUMN_POINTS:
            print(f"点击了队伍积分：{team.TeamName}")

    def handle_button_click(self, index):
        """
        处理按钮点击事件。
        """
        team = self.get_team_at_index(index.row())
        print(f"按钮点击了队伍: {team.TeamName}")

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
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)  # 设置为单选模式
        self.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.horizontalHeader().setStretchLastSection(True)  # 最后一列自动拉伸填充

        # 设置等宽列
        for col in range(self.model.columnCount()):
            self.setColumnWidth(col, 100)  # 设置每列的宽度为 100

        # 设置自定义委托为某些列
        hyperlink_delegate = HyperlinkDelegate(self)
        self.setItemDelegateForColumn(self.model.COLUMN_COMPOSITION, hyperlink_delegate)
        self.setItemDelegateForColumn(self.model.COLUMN_POINTS, hyperlink_delegate)

        button_delegate = ButtonDelegate(self)
        self.setItemDelegateForColumn(self.model.COLUMN_TEAM_NAME, button_delegate)

        # 加载数据
        self.model.fetch_teams()

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
