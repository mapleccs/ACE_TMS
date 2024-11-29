from models.match_pick_ban import MatchPickBan
from sqlalchemy.orm import Session


class MatchPickBanRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_pick_ban(self, pick_ban: MatchPickBan):
        """添加选人禁用记录"""
        self.session.add(pick_ban)
        self.session.commit()
        return pick_ban

    def get_picks_bans_by_match(self, match_id: int):
        """获取比赛的所有选人禁用记录"""
        return self.session.query(MatchPickBan).filter(match_id == MatchPickBan.MatchID).order_by(
            MatchPickBan.PickBanOrder).all()

    def delete_picks_bans_by_match(self, match_id: int):
        """删除比赛的所有选人禁用记录"""
        picks_bans = self.get_picks_bans_by_match(match_id)
        for pb in picks_bans:
            self.session.delete(pb)
        self.session.commit()
