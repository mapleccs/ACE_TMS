from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class Match(Base):
    __tablename__ = 'matches'

    MatchID = Column(Integer, primary_key=True, autoincrement=True)
    HomeTeamID = Column(Integer, ForeignKey('teams.TeamID'), nullable=False)
    AwayTeamID = Column(Integer, ForeignKey('teams.TeamID'), nullable=False)
    MatchDate = Column(DateTime, default=datetime.datetime.utcnow)
    MatchType = Column(String(50), nullable=True)  # 比赛类型，例如 'B01', 'B03', 'BO5'
    WinnerTeamID = Column(Integer, ForeignKey('teams.TeamID'), nullable=True)
    Duration = Column(Integer, nullable=True)  # 比赛时长，单位为秒

    # 关系
    home_team = relationship('Team', foreign_keys=[HomeTeamID], back_populates='matches_as_home')
    away_team = relationship('Team', foreign_keys=[AwayTeamID], back_populates='matches_as_away')
    winner_team = relationship('Team', foreign_keys=[WinnerTeamID])
    picks_bans = relationship('MatchPickBan', back_populates='match', cascade="all, delete-orphan")
    player_stats = relationship('PlayerMatchStats', back_populates='match')

    def __repr__(self):
        return f"<Match(MatchID={self.MatchID}, HomeTeamID={self.HomeTeamID}, AwayTeamID={self.AwayTeamID})>"
