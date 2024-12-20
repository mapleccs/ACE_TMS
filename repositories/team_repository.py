from sqlalchemy import func, case, desc, cast, Integer
from sqlalchemy.sql.functions import current_date

from models import Team, Player, TeamPlayer, TeamSeasonScore, Match
from sqlalchemy.orm import Session, joinedload, aliased


class TeamRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_team(self, team: Team):
        """添加新队伍"""
        self.session.add(team)
        self.session.commit()
        return team

    def get_team_by_id(self, team_id: int):
        """根据ID获取队伍"""
        return self.session.query(Team).filter(Team.ID == team_id).first()

    def get_team_by_name(self, team_name: str):
        """根据名称获取队伍"""
        return self.session.query(Team).filter(Team.TeamName == team_name).first()

    def get_all_teams(self):
        """获取所有队伍"""
        return self.session.query(Team).all()

    def update_team(self, team: Team):
        """更新队伍信息"""
        self.session.commit()
        return team

    def delete_team(self, team: Team):
        """删除队伍"""
        self.session.delete(team)
        self.session.commit()

    def get_all_teams_with_season_detail(self, team_name: str = None, team_abbreviation: str = None):
        """查询队伍基本信息，队伍名称，队伍简称，队长id，联系方式，队伍配置，建队日期，队伍积分，队伍等级，可通过名称和简称模糊查询"""
        team_player = aliased(TeamPlayer)
        team_leader = aliased(Player)
        team = aliased(Team)
        team_season_score = aliased(TeamSeasonScore)

        # 计算队伍的队员数量（去重）并检查是否有队长，并且根据时间过滤，离队的不会记录在内，但是在当前时间点并未离队的会记录在Count内
        all_team_player = aliased(TeamPlayer)
        all_team_count = self.session.query(
            all_team_player.TeamID,
            func.count(func.distinct(all_team_player.PlayerID)).label("teamNum"),
            func.max(
                case(
                    (all_team_player.JobType == 3, 1),
                    else_=0
                )
            ).label("hasLeader")
        ).filter(
            (all_team_player.EndDate.is_(None)) | (func.current_date() < all_team_player.EndDate)
        ).group_by(all_team_player.TeamID).subquery()

        # 获取大局对局数量
        matches_count = self.session.query(
            Team.ID.label('team_id'),
            func.count(func.distinct(Match.MatchDate)).label('matchCount')  # 根据比赛日期去重
        ).join(Match, (Match.HomeTeamID == Team.ID) | (Match.AwayTeamID == Team.ID)) \
            .group_by(Team.ID).subquery()

        # 获取每支队伍在大比赛中的获胜数量
        winner_matches_count = self.session.query(
            Team.ID.label('team_id'),
            func.count(func.distinct(Match.MatchDate)).label('winner_count')  # 根据比赛日期去重
        ).join(Match, (Match.HomeTeamID == Team.ID) | (Match.AwayTeamID == Team.ID)) \
            .filter(Match.WinnerTeamID == Team.ID) \
            .group_by(Team.ID).subquery()

        # 整合数据
        query = self.session.query(
            func.coalesce(team.TeamLogo, "未设置队标").label('teamLogo'),
            team.TeamName,
            team.TeamAbbreviation,
            func.coalesce(team_leader.ID, 0).label('CaptainID'),
            func.coalesce(team_leader.PlayerName, '未设置队长').label('CaptainName'),
            func.coalesce(team_leader.QQ, '未设置队长').label('CaptainQQ'),
            func.coalesce(team_leader.Phone, '未设置手机号').label('CaptainPhone'),
            func.coalesce(all_team_count.c.teamNum, 0).label('teamNum'),
            team.CreateDate,
            func.coalesce(team_season_score.TotalScore, 0).label('TotalScore'),
            func.coalesce(team_season_score.Level, "无等级").label('Level'),
            func.coalesce(all_team_count.c.hasLeader, 0).label('hasLeader'),
            func.coalesce(matches_count.c.matchCount, 0).label('matchCount'),
            func.coalesce(winner_matches_count.c.winner_count, 0).label('winner_count')
        ).select_from(team)

        # 使用左连接，确保即使没有队员数据也能返回队伍信息
        query = query.outerjoin(
            team_player, team.ID == team_player.TeamID
        ).outerjoin(
            team_leader, team_player.PlayerID == team_leader.ID
        ).outerjoin(
            team_season_score, team.ID == team_season_score.TeamID
        ).outerjoin(
            all_team_count, all_team_count.c.TeamID == team.ID
        ).outerjoin(
            matches_count, matches_count.c.team_id == team.ID
        ).outerjoin(
            winner_matches_count, winner_matches_count.c.team_id == team.ID
        )

        # 添加 JobType 的过滤条件，只有当队员存在且有队长时才应用
        query = query.filter(
            case(
                (all_team_count.c.teamNum != 0 and all_team_count.c.hasLeader == 1, team_player.JobType == 3),
                else_=True
            )
        )

        # 添加过滤条件，根据名称或者简称进行过滤
        if team_name:
            query = query.filter(team.TeamName.like(f'%{team_name}%'))
        if team_abbreviation:
            query = query.filter(team.TeamAbbreviation.like(f'%{team_abbreviation}%'))

        # 排序 根据总积分排序 整合返回值
        query = query.with_entities(
            team.TeamName,
            team.TeamAbbreviation,
            func.coalesce(team_leader.PlayerName, '未设置队长').label('captainName'),
            func.coalesce(team_leader.QQ, '未设置队长').label('captainQQ'),
            func.coalesce(all_team_count.c.teamNum, 0).label('teamNum'),
            team.CreateDate,
            func.coalesce(team_season_score.TotalScore, 0).label('totalScore'),
            func.coalesce(team_season_score.Level, "无等级").label('level'),
            func.coalesce(team.TeamLogo, "未设置队标").label('teamLogo'),
            func.coalesce(team_leader.Phone, '未设置手机号').label('CaptainPhone'),
            func.coalesce(matches_count.c.matchCount, 0).label('matchCount'),
            func.coalesce(winner_matches_count.c.winner_count, 0).label('winner_count')
        ).order_by(
            desc(team_season_score.TotalScore)
        )

        result = query.all()

        result_dicts = [
            {
                'teamName': row[0],
                'teamAbbreviation': row[1],
                'captainName': row[2],
                'captainQQ': row[3],
                'teamNum': row[4],
                'createDate': row[5],
                'totalScore': row[6],
                'level': row[7],
                'teamLogo': row[8],
                'captainPhone': row[9],
                'matchCount': row[10],
                'winnerCount': row[11]
            }
            for row in result
        ]

        return result_dicts
