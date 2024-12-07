from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class MatchType(Base):
    __tablename__ = 'match_type'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), nullable=False, unique=True)

    matches = relationship('Match', back_populates='match_type')

    def __repr__(self):
        return f"<MatchType(ID={self.ID}, Name={self.Name})>"
