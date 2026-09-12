from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database.database import Base, engine, SessionLocal
from app.models.alert import Alert
from app.models.security_event_db import SecurityEventDB
from app.models.security_event import SecurityEvent
from app.detection.brute_force import detect_brute_force

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

    recent_events = db.query(SecurityEventDB).all()

    alerts = detect_brute_force(recent_events)

    for alert in alerts:
        existing_alert = (
            db.query(Alert)
            .filter(
                Alert.alert_type == alert["type"],
                Alert.source_ip == alert["source_ip"],
                Alert.status == "open",
            )
            .first()
        )

        if existing_alert is None:
            db.add(
                Alert(
                    timestamp=event.timestamp,
                    alert_type=alert["type"],
                    severity=alert["severity"],
                    source_ip=alert["source_ip"],
                    attempts=alert["attempts"],
                    description=alert["description"],
                )
            )

    db.commit()

    return {
        "message": "Security event stored successfully",
        "event_id": db_event.id,
        "alerts": alerts
    }


@app.get("/events")
def get_events(db: Session = Depends(get_db)):

    events = db.query(SecurityEventDB).all()

    return events


@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    """Return saved alerts with the newest alerts first."""
    return db.query(Alert).order_by(Alert.timestamp.desc()).all()
