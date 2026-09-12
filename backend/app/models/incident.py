from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from app.database.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    severity = Column(String, nullable=False, default="medium")
    status = Column(String, nullable=False, default="open")
    source_ip = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
