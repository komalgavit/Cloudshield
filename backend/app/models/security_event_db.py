from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base


class SecurityEventDB(Base):
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    source_ip = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    username = Column(String, nullable=True)
    severity = Column(String, nullable=False, default="low")
    description = Column(String, nullable=False)