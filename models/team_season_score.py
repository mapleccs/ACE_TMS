from sqlalchemy import Column, Integer, ForeignKey,String
from .base import Base

class TeamSeasonScore(Base):
    __tablename__ = 'teamSeasonScore'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    TeamID = Column(Integer, ForeignKey('team.ID'), nullable=False)
    SeasonID = Column(Integer, ForeignKey('season.ID'), nullable=False)
    TotalScore = Column(Integer, nullable=False)
    TotalSpecial = Column(Integer, nullable=False)
    Level = Column(String(10), nullable=True)

    def __repr__(self):
        return f"<TeamSeasonScore(ID={self.ID}, TeamID={self.TeamID}, SeasonID={self.SeasonID})>"
