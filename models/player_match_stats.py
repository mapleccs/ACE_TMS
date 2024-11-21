from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from .base import Base


class PlayerMatchStats(Base):
    __tablename__ = 'player_match_stats'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    MatchID = Column(Integer, ForeignKey('matches.MatchID'), nullable=False)
    PlayerID = Column(Integer, ForeignKey('players.PlayerID'), nullable=False)
    TeamID = Column(Integer, ForeignKey('teams.TeamID'), nullable=False)
    HeroID = Column(Integer, ForeignKey('heroes.HeroID'), nullable=False)
    Position = Column(String(20), nullable=True)  # 位置，例如 'Top', 'Jungle'

    # 统计数据
    Kills = Column(Integer, default=0)
    Deaths = Column(Integer, default=0)
    Assists = Column(Integer, default=0)
    DamageDealt = Column(Integer, default=0)  # 造成的伤害值
    DamageTaken = Column(Integer, default=0)  # 承受的伤害值
    DamageToTakenRatio = Column(Float, default=0.0)  # 伤害转化比
    VisionScore = Column(Integer, default=0)  # 视野得分
    GoldEarned = Column(Integer, default=0)
    CS = Column(Integer, default=0)  # 补刀数
    WardsPlaced = Column(Integer, default=0)
    WardsKilled = Column(Integer, default=0)

    # 关系
    match = relationship('Match', back_populates='player_stats')
    player = relationship('Player', back_populates='match_stats')
    team = relationship('Team')
    hero = relationship('Hero')

    def __repr__(self):
        return f"<PlayerMatchStats(MatchID={self.MatchID}, PlayerID={self.PlayerID}, HeroID={self.HeroID})>"
