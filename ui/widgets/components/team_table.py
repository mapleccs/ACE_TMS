from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import QAbstractTableModel, Qt


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
        if teams is None:
            self.teams = []
        else:
            self.teams = teams
        self.endResetModel()

    def rowCount(self, parent=None):
        if self.teams is None:
            return 0
        return len(self.teams)

    def columnCount(self, parent=None):
        return 2  # 队伍ID和队伍名称

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        team = self.teams[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return team.TeamID
            elif index.column() == 1:
                return team.TeamName
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return "队伍ID"
            elif section == 1:
                return "队伍名称"
        return None

    def get_team_at_index(self, row):
        if 0 <= row < len(self.teams):
            return self.teams[row]
        return None
