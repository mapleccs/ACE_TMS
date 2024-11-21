from models.match import Match
from sqlalchemy.orm import Session


class MatchRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_match(self, match: Match):
        """添加新比赛"""
        self.session.add(match)
        self.session.commit()
        return match

    def get_match_by_id(self, match_id: int):
        """根据ID获取比赛"""
        return self.session.query(Match).filter(Match.MatchID == match_id).first()

    def get_all_matches(self):
        """获取所有比赛"""
        return self.session.query(Match).all()

    def update_match(self, match: Match):
        """更新比赛信息"""
        self.session.commit()
        return match

    def delete_match(self, match: Match):
        """删除比赛"""
        self.session.delete(match)
        self.session.commit()
