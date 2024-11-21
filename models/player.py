from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from . import Base
import datetime


class Player(Base):
    __tablename__ = 'players'

    PlayerID = Column(Integer, primary_key=True, autoincrement=True)
    PlayerName = Column(String(50), nullable=False, unique=True)
    CreatedAt = Column(DateTime, default=datetime.datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    team_players = relationship('TeamPlayer', back_populates='player')
    match_stats = relationship('PlayerMatchStat', back_populates='player')
