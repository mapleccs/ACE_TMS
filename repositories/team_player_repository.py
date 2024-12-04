from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, case, desc, cast, Integer
from datetime import datetime
from models import Team, Player, TeamPlayer, PlayerReasonScore


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

    def get_team_player_with_season_detail_by_team(self, team_id: int):
        """根据teamID查询队伍的成员， 显示成员名称，偏好位置，游戏id，个人积分（总），队内职位"""

        team_player = aliased(TeamPlayer)
        player = aliased(Player)
        player_reason_score = aliased(PlayerReasonScore)


        query = self.session.query(
            player.ID,
            player.PlayerName,
            player.PreferredRoles,
            player.InGameName,
            player_reason_score.TotalScore,
            team_player.JobType,
        ).select_from(player).outerjoin(
            team_player, team_player.PlayerID == player.ID
        ).outerjoin(
            player_reason_score, player_reason_score.PlayerID == player.ID
        ).filter(
            team_player.TeamID == team_id,
        )


        result = query.all()

        result_dicts = [
            {
                'playerId': row[0],
                'playerName': row[1],
                'preferredRoles': row[2],
                'inGameName': row[3],
                'totalScore': row[4],
                'jobType': row[5],
            }
            for row in result
        ]

        return result_dicts

