import time
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="PiConsensus On-Chain Audit Trail & Forensics Engine", version="1.0")

# === Database Setup (SQLite for demo, switch to PostgreSQL in prod) ===

DATABASE_URL = "sqlite:///./audit_trail.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class AuditEventDB(Base):
    __tablename__ = "audit_events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True# === Pydantic Models ===

class AuditEvent(BaseModel):
    event_type: str
    subject: str
    data: Dict[str, Any]
    timestamp: float = time.time()

# === API Endpoints ===

@app.post("/audit/log")
def log_event(event: AuditEvent):
    db_event = AuditEventDB(
        event_type=event.event_type,
        subject=event.subject,
        data=str(event.data),
        timestamp=event.timestamp
    )
    session.add(db_event)
    session.commit()
    return {"status": "logged", "event_id": db_event.id}

@app.get("/audit/search")
def search_events(
    subject: Optional[str] = None,
    event_type: Optional[str] = None,
    start_time: Optional[float] = None,
    end_time: Optional[float] = None,
    limit: int = Query(50, le=200)
):
    query = session.query(AuditEventDB)
    if subject:
        query = query.filter(AuditEventDB.subject == subject)
    if event_type:
        query = query.filter(AuditEventDB.event_type == event_type)
    if start_time:
        query = query.filter(AuditEventDB.timestamp >= start_time)
    if end_time:
        query = query.filter(AuditEventDB.timestamp <= end_time)
    events = query.order_by(desc(AuditEventDB.timestamp)).limit(limit).all()
    return [
        {
            "id": e.id,
            "event_type": e.event_type,
            "subject": e.subject,
            "data": e.data,
            "timestamp": e.timestamp
        }
        for e in events
    ]

@app.get("/audit/forensics_report")
def forensics_report(subject: str):
    """Generate a simple forensics report for a subject."""
    query = session.query(AuditEventDB).filter(AuditEventDB.subject == subject).order_by(AuditEventDB.timestamp)
    events = query.all()
    return {
        "subject": subject,
        "n_events": len(events),
        "timeline": [
            {
                "event_type": e.event_type,
                "data": e.data,
                "timestamp": e.timestamp
            } for e in events
        ]
    }

@app.get("/audit/recent")
def recent_events(limit: int = 20):
    events = session.query(AuditEventDB).order_by(desc(AuditEventDB.timestamp)).limit(limit).all()
    return [
        {
            "id": e.id,
            "event_type": e.event_type,
            "subject": e.subject,
            "data": e.data,
            "timestamp": e.timestamp
        }
        for e in events
    ]

# === Example Run: uvicorn src.forensics.audit_trail:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("forensics.audit_trail:app", host="0.0.0.0", port=8005, reload=True)
