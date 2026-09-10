from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    alert_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    source_ip = Column(String, nullable=False)
    attempts = Column(Integer, nullable=True)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="open")