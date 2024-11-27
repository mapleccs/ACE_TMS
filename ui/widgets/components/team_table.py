from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import Qt, QAbstractTableModel


class TeamTable(QTableView):
    def __init__(self):
        super().__init__()
        self.model = TeamTableModel()
        self.setModel(self.model)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)

    def set_teams(self, teams):
        self.model.set_teams(teams)

    def get_selected_team(self):
        index = self.currentIndex()
        if index.isValid():
            return self.model.get_team_at_index(index.row())
        return None


class TeamTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.teams = []

    def set_teams(self, teams):
        self.beginResetModel()
        self.teams = teams
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self.teams)

    def columnCount(self, parent=None):
        return 7  # 队名、队长、队长联系方式、队伍配置、建队日期、队伍积分、队伍等级

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        team = self.teams[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return team['队伍名称']
            elif index.column() == 1:
                return team['队长ID']
            elif index.column() == 2:
                return team['联系方式']
            elif index.column() == 3:
                return team['队伍配置']
            elif index.column() == 4:
                return team['建队日期']
            elif index.column() == 5:
                return team['队伍积分']
            elif index.column() == 6:
                return team['队伍等级']
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return "队伍名称"
            elif section == 1:
                return "队长ID"
            elif section == 2:
                return "联系方式"
            elif section == 3:
                return "队伍配置"
            elif section == 4:
                return "建队日期"
            elif section == 5:
                return "队伍积分"
            elif section == 6:
                return "队伍等级"
        return None

    def get_team_at_index(self, row):
        if 0 <= row < len(self.teams):
            return self.teams[row]
        return None
