from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class MatchPickBan(Base):
    __tablename__ = 'matchPickBan'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    MatchID = Column(Integer, ForeignKey('match.ID'), nullable=False)
    TeamID = Column(Integer, ForeignKey('team.ID'), nullable=False)
    HeroID = Column(Integer, ForeignKey('hero.ID'), nullable=False)
    IsPick = Column(Integer, nullable=False)  # 1: Pick, 0: Ban
    Round = Column(Integer, nullable=False)
    PickBanOrder = Column(Integer, nullable=False)
    PlayerID = Column(Integer, ForeignKey('player.ID'), nullable=True)

    match = relationship('Match', back_populates='picks_bans')
    team = relationship('Team')
    hero = relationship('Hero')
    player = relationship('Player')

    def __repr__(self):
        return f"<MatchPickBan(ID={self.ID}, MatchID={self.MatchID}, TeamID={self.TeamID})>"
