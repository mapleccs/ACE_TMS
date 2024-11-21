from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class TeamPlayer(Base):
    __tablename__ = 'team_players'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    TeamID = Column(Integer, ForeignKey('teams.TeamID'), nullable=False)
    PlayerID = Column(Integer, ForeignKey('players.PlayerID'), nullable=False)
    StartDate = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    EndDate = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint('PlayerID', 'StartDate', name='uix_player_startdate'),
    )

    # 关系
    team = relationship('Team', back_populates='team_players')
    player = relationship('Player', back_populates='team_players')

    def __repr__(self):
        return f"<TeamPlayer(TeamID={self.TeamID}, PlayerID={self.PlayerID})>"
