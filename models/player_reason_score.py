from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class PlayerReasonScore(Base):
    __tablename__ = 'playerReasonScore'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    PlayerID = Column(Integer, ForeignKey('player.ID'), nullable=False)
    SeasonID = Column(Integer, ForeignKey('season.ID'), nullable=False)
    TotalScore = Column(Integer, nullable=False)
    UpdateDate = Column(DateTime, default=datetime.datetime.utcnow)

    player = relationship('Player', back_populates='reason_scores')
    season = relationship('Season')

    def __repr__(self):
        return f"<PlayerReasonScore(ID={self.ID}, PlayerID={self.PlayerID})>"
