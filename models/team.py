from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from . import Base
import datetime


class Team(Base):
    __tablename__ = 'teams'

    TeamID = Column(Integer, primary_key=True, autoincrement=True)
    TeamName = Column(String(50), nullable=False, unique=True)
    TeamStatus = Column(String(20), default='active', nullable=False)
    CreatedAt = Column(DateTime, default=datetime.datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    team_players = relationship('TeamPlayer', back_populates='team')
    matches_home = relationship('Match', back_populates='home_team', foreign_keys='Match.HomeTeamID')
    matches_away = relationship('Match', back_populates='away_team', foreign_keys='Match.AwayTeamID')
