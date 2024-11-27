from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .team_player import TeamPlayer


class Team(Base):
    __tablename__ = 'team'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    TeamName = Column(String(50), nullable=False, unique=True)
    TeamLogo = Column(String(500), nullable=True)
    PlayerID = Column(Integer, ForeignKey('player.ID'), nullable=False)
    TeamState = Column(Integer, nullable=False, default=0)  # 0: 在役, 1: 注销, 2: 冻结

    creator = relationship('Player', back_populates='created_teams')
    members = relationship('TeamPlayer', back_populates='team', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Team(ID={self.ID}, TeamName={self.TeamName})>"

