from repositories.team_player_repository import TeamPlayerRepository
from models.team_player import TeamPlayer
from sqlalchemy.orm import Session

"""队伍成员表service层"""
"""表格功能：队伍表和玩家表的关联关系"""
class TeamPlayerService:
    def __init__(self, session: Session):
        self.session = session
        self.team_player_repository = TeamPlayerRepository(session)

    def get_all_team_players(self, entity: TeamPlayer):
        return self.team_player_repository.get_all_team_players()

    def add_team_player(self, entity: TeamPlayer):
        ## team_player = TeamPlayer(TeamPlayerName=team_player_name)
        return self.team_player_repository.add_team_player(entity)

    def update_team_player(self, entity: TeamPlayer):
        team_player = self.team_player_repository.get_team_player_by_id(entity.ID)
        if team_player:
            ## team_player.TeamPlayerName = new_name
            return self.team_player_repository.update_team_player(entity)
        else:
            return None

    def delete_team_player(self, team_player_id: int):
        team_player = self.team_player_repository.get_team_player_by_id(team_player_id)
        if team_player:
            self.team_player_repository.delete_team_player(team_player)
            return True
        else:
            return False
