import logging

logging.basicConfig(level=logging.DEBUG)


def set_teams(self, teams):
    logging.debug(f"set_teams called with teams: {teams}")
    self.beginResetModel()
    self.teams = teams if teams is not None else []
    self.endResetModel()
