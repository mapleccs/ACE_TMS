from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class Match(Base):
    __tablename__ = 'match'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    HomeTeamID = Column(Integer, ForeignKey('team.ID'), nullable=False)
    AwayTeamID = Column(Integer, ForeignKey('team.ID'), nullable=False)
    MatchDate = Column(DateTime, default=datetime.datetime.utcnow)
    MatchType = Column(String(50), nullable=True)  # 比赛类型
    WinnerTeamID = Column(Integer, ForeignKey('team.ID'), nullable=True)
    Duration = Column(Integer, nullable=True)  # 秒
    SeasonID = Column(Integer, ForeignKey('season.ID'), nullable=False)

    season = relationship('Season', back_populates='matches')
    home_team = relationship('Team', foreign_keys=[HomeTeamID], back_populates='matches_as_home')
    away_team = relationship('Team', foreign_keys=[AwayTeamID], back_populates='matches_as_away')
    winner_team = relationship('Team', foreign_keys=[WinnerTeamID])

    picks_bans = relationship('MatchPickBan', back_populates='match', cascade="all, delete-orphan")

    player_stats = relationship('PlayerMatchStats', back_populates='match', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Match(ID={self.ID}, HomeTeamID={self.HomeTeamID}, AwayTeamID={self.AwayTeamID})>"
