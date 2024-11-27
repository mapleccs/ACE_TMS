from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class PlayerReasonScoreDetail(Base):
    __tablename__ = 'playerReasonScoreDetail'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    PlayerScoreID = Column(Integer, ForeignKey('playerReasonScore.ID'), nullable=False)
    IsAdd = Column(Integer, nullable=False)
    Value = Column(Integer, nullable=False)
    CreateDate = Column(DateTime, default=datetime.datetime.utcnow)
    Reason = Column(String(200), nullable=True)

    reason_score = relationship('PlayerReasonScore')

    def __repr__(self):
        return f"<PlayerReasonScoreDetail(ID={self.ID}, PlayerScoreID={self.PlayerScoreID})>"
