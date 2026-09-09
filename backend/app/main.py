from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database.database import Base, engine, SessionLocal
from app.models.security_event_db import SecurityEventDB
from app.models.security_event import SecurityEvent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CloudShield")


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "CloudShield is running!"}


@app.post("/events")
def create_event(event: SecurityEvent, db: Session = Depends(get_db)):

    db_event = SecurityEventDB(
        timestamp=event.timestamp,
        source_ip=event.source_ip,
        event_type=event.event_type,
        username=event.username,
        severity=event.severity,
        description=event.description
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return {
        "message": "Security event stored successfully",
        "event_id": db_event.id
    }


@app.get("/events")
def get_events(db: Session = Depends(get_db)):

    events = db.query(SecurityEventDB).all()

    return events