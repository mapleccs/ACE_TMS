from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
import datetime


class Match(Base):
    __tablename__ = 'matches'

    MatchID = Column(Integer, primary_key=True, autoincrement=True)
    TournamentID = Column(Integer, ForeignKey('tournaments.TournamentID'), nullable=True)
    HomeTeamID = Column(Integer, ForeignKey('teams.TeamID'), nullable=False)
    AwayTeamID = Column(Integer, ForeignKey('teams.TeamID'), nullable=False)
    MatchDate = Column(DateTime, default=datetime.datetime.utcnow)
    MatchType = Column(String(50), nullable=True)
    Result = Column(String(10), nullable=True)  # e.g., 'Win', 'Lose', 'Draw'
    CreatedAt = Column(DateTime, default=datetime.datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    match_bans = relationship('MatchBan', back_populates='match')
    match_picks = relationship('MatchPick', back_populates='match')
    player_stats = relationship('PlayerMatchStat', back_populates='match')
    tournament = relationship('Tournament', back_populates='matches')
    home_team = relationship('Team', back_populates='matches_home', foreign_keys=[HomeTeamID])
    away_team = relationship('Team', back_populates='matches_away', foreign_keys=[AwayTeamID])
