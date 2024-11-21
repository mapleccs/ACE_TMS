from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint, String
from sqlalchemy.orm import relationship
from . import Base
import datetime


class TeamPlayer(Base):
    __tablename__ = 'team_players'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    TeamID = Column(Integer, ForeignKey('teams.TeamID'), nullable=False)
    PlayerID = Column(Integer, ForeignKey('players.PlayerID'), nullable=False)
    StartDate = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    EndDate = Column(DateTime, nullable=True)
    Role = Column(String(50), nullable=True)

    __table_args__ = (
        UniqueConstraint('PlayerID', 'StartDate', name='uix_player_startdate'),
    )

    team = relationship('Team', back_populates='team_players')
    player = relationship('Player', back_populates='team_players')
