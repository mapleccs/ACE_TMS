from sqlalchemy import Column, Integer, ForeignKey,DateTime, String
from .base import Base

class TeamMemberRoleChangeRecord(Base):
    __tablename__ = 'teamMemberRoleChangeRecord'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    TeamPlayerID = Column(Integer, ForeignKey('teamPlayer.ID'), nullable=False)
    OldRole = Column(String(50), nullable=False)
    NewRole = Column(String(50), nullable=False)
    ChangeDate = Column(DateTime, nullable=False)
    Reason = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<TeamMemberRoleChangeRecord(ID={self.ID}, TeamPlayerID={self.TeamPlayerID})>"
