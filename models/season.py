from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class Season(Base):
    __tablename__ = 'season'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    SeasonName = Column(String(50), nullable=False)
    StartDate = Column(DateTime, nullable=False)
    EndDate = Column(DateTime, nullable=False)
    State = Column(Integer, nullable=False, default=0)  # 0: 进行中, 1: 未开始, 2: 已结束

    matches = relationship('Match', back_populates='season', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Season(ID={self.ID}, SeasonName={self.SeasonName})>"
