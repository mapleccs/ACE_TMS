from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Player(Base):
    __tablename__ = 'player'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    PlayerName = Column(String(50), nullable=False, unique=True)
    InGameName = Column(String(50), nullable=True)
    PreferredRoles = Column(String(100), nullable=True)
    QQ = Column(String(50), nullable=False)
    Phone = Column(String(50), nullable=True)

    created_teams = relationship('Team', back_populates='creator')
    matches_stats = relationship('PlayerMatchStats', back_populates='player', cascade="all, delete-orphan")
    picks_bans = relationship('MatchPickBan', back_populates='player')
    reason_scores = relationship('PlayerReasonScore', back_populates='player', cascade="all, delete-orphan")
    team_memberships = relationship('TeamPlayer', back_populates='player', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Player(ID={self.ID}, PlayerName={self.PlayerName})>"
