from sqlalchemy import Column, Integer, ForeignKey
from . import Base


class MatchBan(Base):
    __tablename__ = 'match_bans'

    MatchID = Column(Integer, ForeignKey('matches.MatchID'), primary_key=True)
    TeamID = Column(Integer, ForeignKey('teams.TeamID'), primary_key=True)
    HeroID = Column(Integer, ForeignKey('heroes.HeroID'), primary_key=True)
    BanOrder = Column(Integer)
