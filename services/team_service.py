from repositories import TeamRepository
from models.team import Team


class TeamService:
    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository

    def get_all_teams(self):
        return self.team_repository.get_all_teams()

    def add_team(self, team_name: str):
        team = Team(TeamName=team_name)
        return self.team_repository.add_team(team)

    def update_team(self, team_id: int, new_name: str):
        team = self.team_repository.get_team_by_id(team_id)
        if team:
            team.TeamName = new_name
            return self.team_repository.update_team(team)
        else:
            return None

    def delete_team(self, team_id: int):
        team = self.team_repository.get_team_by_id(team_id)
        if team:
            self.team_repository.delete_team(team)
            return True
        else:
            return False