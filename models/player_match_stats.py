from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from .base import Base

class PlayerMatchStats(Base):
    __tablename__ = 'playerMatchStats'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    MatchID = Column(Integer, ForeignKey('match.ID'), nullable=False)
    PlayerID = Column(Integer, ForeignKey('player.ID'), nullable=False)
    TeamID = Column(Integer, ForeignKey('team.ID'), nullable=False)
    HeroID = Column(Integer, ForeignKey('hero.ID'), nullable=False)
    Position = Column(String(20), nullable=True)

    #统计数据
    Kills = Column(Integer, default=0)
    Deaths = Column(Integer, default=0)
    Assists = Column(Integer, default=0)
    DamageDealt = Column(Integer, default=0)
    DamageTaken = Column(Integer, default=0)
    DamageToTakenRatio = Column(Float, default=0)
    VisionScore = Column(Integer, default=0)
    GoldEarned = Column(Integer, default=0)
    CS = Column(Integer, default=0)
    WardsPlaces = Column(Integer, default=0)
    WardsKilled = Column(Integer, default=0)

    # 关系
    match = relationship('Match', back_populates='player_stats')
    player = relationship('Player', back_populates='matches_stats')
    team = relationship('Team')
    hero = relationship('Hero', back_populates='player_stats')

    def __repr__(self):
        return f"<PlayerMatchStats(ID={self.ID}, MatchID={self.MatchID}, PlayerID={self.PlayerID})>"
