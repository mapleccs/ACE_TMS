from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class MatchPickBan(Base):
    __tablename__ = 'match_pick_bans'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    MatchID = Column(Integer, ForeignKey('matches.MatchID'), nullable=False)  # 关联比赛
    TeamID = Column(Integer, ForeignKey('teams.TeamID'), nullable=False)  # 关联队伍
    HeroID = Column(Integer, ForeignKey('heroes.HeroID'), nullable=False)  # 关联英雄
    IsPick = Column(Boolean, nullable=False)  # True: 选人 / False: 禁用
    Round = Column(Integer, nullable=False)  # 哪一轮操作（如第1轮ban，第1轮pick等）
    PickBanOrder = Column(Integer, nullable=False)  # 每队的选禁顺序，0表示第一个，9表示第十个
    PlayerID = Column(Integer, ForeignKey('players.PlayerID'), nullable=True)  # 只有选人时才会有玩家ID

    # 关系
    match = relationship('Match', back_populates='picks_bans')
    team = relationship('Team')
    hero = relationship('Hero')
    player = relationship('Player')

    def __repr__(self):
        return f"<MatchPickBan(MatchID={self.MatchID}, TeamID={self.TeamID}, HeroID={self.HeroID}, IsPick={self.IsPick}, Round={self.Round}, PickBanOrder={self.PickBanOrder})>"
