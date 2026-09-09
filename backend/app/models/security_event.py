from pydantic import BaseModel
from datetime import datetime


class SecurityEvent(BaseModel):
    timestamp: datetime
    source_ip: str
    event_type: str
    username: str | None = None
    severity: str = "low"
    description: str