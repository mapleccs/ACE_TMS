from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Player(Base):
    __tablename__ = 'players'

    PlayerID = Column(Integer, primary_key=True, autoincrement=True)
    PlayerName = Column(String(50), nullable=False, unique=True)
    InGameName = Column(String(50), nullable=True)  # 游戏内昵称
    PreferredRoles = Column(String(100), nullable=True)  # 偏好的位置，例如 'Top, Jungle'

    # 关系
    team_players = relationship('TeamPlayer', back_populates='player')
    match_stats = relationship('PlayerMatchStats', back_populates='player')

    def __repr__(self):
        return f"<Player(PlayerID={self.PlayerID}, PlayerName='{self.PlayerName}')>"
