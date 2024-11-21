from sqlalchemy import Column, Integer, DateTime, ForeignKey
from . import Base
import datetime


class PlayerMatchStat(Base):
    __tablename__ = 'player_match_stats'

    MatchID = Column(Integer, ForeignKey('matches.MatchID'), primary_key=True)
    PlayerID = Column(Integer, ForeignKey('players.PlayerID'), primary_key=True)
    TeamID = Column(Integer, ForeignKey('teams.TeamID'))
    DamageDealt = Column(Integer)
    DamageTaken = Column(Integer)
    WardsPlaced = Column(Integer)
    Kills = Column(Integer)
    Deaths = Column(Integer)
    Assists = Column(Integer)
    GoldEarned = Column(Integer)
    CreepScore = Column(Integer)
    CreatedAt = Column(DateTime, default=datetime.datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
