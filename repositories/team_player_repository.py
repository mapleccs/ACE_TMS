from ..models.team_player import TeamPlayer
from sqlalchemy.orm import Session
from datetime import datetime


class TeamPlayerRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_team_player(self, team_player: TeamPlayer):
        """将玩家添加到队伍"""
        self.session.add(team_player)
        self.session.commit()
        return team_player

    def get_current_team_player(self, player_id: int):
        """获取玩家当前所属的队伍"""
        return self.session.query(TeamPlayer).filter(
            player_id == TeamPlayer.PlayerID,
            TeamPlayer.EndDate == None
        ).first()

    def get_team_players_by_team(self, team_id: int):
        """获取队伍的所有当前成员"""
        return self.session.query(TeamPlayer).filter(
            team_id == TeamPlayer.TeamID,
            TeamPlayer.EndDate == None
        ).all()

    def remove_player_from_team(self, player_id: int):
        """将玩家从队伍中移除"""
        team_player = self.get_current_team_player(player_id)
        if team_player:
            team_player.EndDate = datetime.utcnow()
            self.session.commit()
            return True
        return False
