from sqlalchemy import Column, Integer, String
from . import Base


class Hero(Base):
    __tablename__ = 'heroes'

    HeroID = Column(Integer, primary_key=True, autoincrement=True)
    HeroName = Column(String(50), nullable=False)
    HeroAlias = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Hero(HeroID={self.HeroID}, HeroName='{self.HeroName}')>"
