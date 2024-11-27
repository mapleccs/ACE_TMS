from models.team import Team
from sqlalchemy.orm import Session


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
