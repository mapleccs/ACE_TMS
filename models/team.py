from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .team_player import TeamPlayer


class Team(Base):
    __tablename__ = 'teams'

    TeamID = Column(Integer, primary_key=True, autoincrement=True)
    TeamName = Column(String(50), nullable=False, unique=True)
    TeamLogo = Column(String(200), nullable=True)  # 队伍Logo的URL

    # 关系
    team_players = relationship('TeamPlayer', back_populates='team')
    matches_as_home = relationship('Match', back_populates='home_team', foreign_keys='Match.HomeTeamID')
    matches_as_away = relationship('Match', back_populates='away_team', foreign_keys='Match.AwayTeamID')

    def __repr__(self):
        return f"<Team(TeamID={self.TeamID}, TeamName='{self.TeamName}')>"
