from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Hero(Base):
    __tablename__ = 'hero'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    HeroName = Column(String(50), nullable=False)
    HeroAlias = Column(String(50), nullable=False)

    picks_bans = relationship('MatchPickBan', back_populates='hero')
    player_stats = relationship('PlayerMatchStats', back_populates='hero')

    def __repr__(self):
        return f"<Hero(ID={self.ID}, HeroName={self.HeroName})>"
