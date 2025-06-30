import time
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.ensemble import IsolationForest
import numpy as np

app = FastAPI(title="PiConsensus AI Intrusion Detection", version="1.0")

# === Data Models ===

class NetworkEvent(BaseModel):
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    packet_size: int
    timestamp: float = time.time()

class Alert(BaseModel):
    event: Dict[str, Any]
    score: float
    reason: str
    timestamp: float

# === In-Memory Event and Alert Store ===

network_events: List[NetworkEvent] = []
alerts: List[Alert] = []

# === AI/ML IDS Engine ===

class IntrusionDetector:
    def __init__(self):
        self.model = IsolationForest(n_estimators=100, contamination=0.05)
        self.trained = False

    def fit(self, events: List[NetworkEvent]):
        if len(events) < 10:
            return
        X = np.array([[e.src_port, e.dst_port, e.packet_size] for e in events])
        self.model.fit(X)
        self.trained = True

    def detect(self, event: NetworkEvent) -> float:
        if not self.trained:
            return 0.0
        X = np.array([[event.src_port, event.dst_port, event.packet_size]])
        score = self.model.decision_function(X)[0]
        return score

ids_engine = IntrusionDetector()

# === API Endpoints ===

@app.post("/event")
def post_event(ev: NetworkEvent):
    network_events.append(ev)
    # Retrain model periodically (every 50 events)
    if len(network_events) % 50 == 0:
        ids_engine.fit(network_events[-500:])  # Use last 500 events for sliding window
    # Detect anomaly
    if ids_engine.trained:
        score = ids_engine.detect(ev)
        if score < -0.2:
            alert = Alert(event=ev.dict(), score=score, reason="Anomaly detected", timestamp=time.time())
            alerts.append(alert)
            return {"alert": True, "score": score, "msg": "Potential intrusion detected"}
    return {"alert": False}

@app.get("/alerts")
def get_alerts(limit: int = 20):
    return [a.dict() for a in alerts[-limit:]]

@app.get("/events")
def get_events(limit: int = 50):
    return [e.dict() for e in network_events[-limit:]]

@app.get("/status")
def get_status():
    return {
        "total_events": len(network_events),
        "alerts": len(alerts),
        "model_trained": ids_engine.trained
    }

# === Example Run: uvicorn src.defense.ai_intrusion_detection:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("defense.ai_intrusion_detection:app", host="0.0.0.0", port=8004, reload=True)
