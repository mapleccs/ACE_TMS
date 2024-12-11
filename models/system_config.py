from sqlalchemy import Column, String, DateTime
from .base import Base


class SystemConfig(Base):
    __tablename__ = 'systemConfig'

    config_id = Column(String(64), primary_key=True)
    create_by = Column(String(64), nullable=True)
    create_time = Column(DateTime, nullable=True)
    remark = Column(String(500), nullable=True)
    update_by = Column(String(64), nullable=True)
    update_time = Column(DateTime, nullable=True)
    config_code = Column(String(100), nullable=True)
    config_name = Column(String(100), nullable=True)
    config_type = Column(String(100), nullable=True)
    config_value = Column(String(600), nullable=True)

    def __repr__(self):
        return f"<SystemConfig(config_id={self.config_id})>"
