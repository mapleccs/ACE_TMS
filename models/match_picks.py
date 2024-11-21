from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base


class MatchPick(Base):
    __tablename__ = 'match_picks'

    MatchID = Column(Integer, ForeignKey('matches.MatchID'), primary_key=True)
    PlayerID = Column(Integer, ForeignKey('players.PlayerID'), primary_key=True)
    TeamID = Column(Integer, ForeignKey('teams.TeamID'))
    HeroID = Column(Integer, ForeignKey('heroes.HeroID'))
    PickOrder = Column(Integer)
    Role = Column(String(20))
