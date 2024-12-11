from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class TeamPlayer(Base):
    __tablename__ = 'teamPlayer'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    TeamID = Column(Integer, ForeignKey('team.ID'), nullable=False)
    PlayerID = Column(Integer, ForeignKey('player.ID'), nullable=False)
    JobType = Column(Integer, default=0)  # 0: 队员, 1: 副队长, 2: 队长
    StartDate = Column(DateTime, default=datetime.datetime.utcnow)
    EndDate = Column(DateTime, nullable=True)

    team = relationship('Team', back_populates='members')
    player = relationship('Player', back_populates='team_memberships')

    def __repr__(self):
        return f"<TeamPlayer(ID={self.ID}, TeamID={self.TeamID}, PlayerID={self.PlayerID})>"
