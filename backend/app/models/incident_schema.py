from pydantic import BaseModel


class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str = "medium"
    status: str = "open"
    source_ip: str | None = None
    