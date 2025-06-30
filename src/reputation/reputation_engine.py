import time
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="PiConsensus Decentralized Reputation & Trust Engine", version="1.0")

# === Data Models ===

class TrustEvent(BaseModel):
    id: int
    subject: str        # The address, agent, or entity whose reputation is affected
    event_type: str     # e.g. "vote", "validate", "slash", "reward", "report"
    delta: float        # How much to increase/decrease trust
    reason: Optional[str] = None
    timestamp: float = time.time()
    actor: Optional[str] = None    # Who caused this event (optional)

class ReputationScore(BaseModel):
    subject: str
    score: float
    last_updated: float = time.time()

# === In-memory Store (replace with DB in production) ===

reputation_scores: Dict[str, ReputationScore] = {}
trust_events: List[TrustEvent] = []
event_counter = 1

# === API Endpoints ===

@app.post("/reputation/event")
def add_trust_event(subject: str, event_type: str, delta: float, reason: Optional[str] = None, actor: Optional[str] = None):
    global event_counter
    # Update or create reputation score
    rep = reputation_scores.get(subject)
    if rep is None:
        rep = ReputationScore(subject=subject, score=0.0)
        reputation_scores[subject] = rep
    rep.score += delta
    rep.last_updated = time.time()
    # Record trust event
    event = TrustEvent(
        id=event_counter,
        subject=subject,
        event_type=event_type,
        delta=delta,
        reason=reason,
        timestamp=rep.last_updated,
        actor=actor
    )
    trust_events.append(event)
    event_counter += 1
    return {"status": "updated", "subject": subject, "score": rep.score, "event_id": event.id}

@app.get("/reputation/score/{subject}")
def get_reputation_score(subject: str):
    rep = reputation_scores.get(subject)
    if not rep:
        raise HTTPException(404, "Subject not found")
    return rep.dict()

@app.get("/reputation/history/{subject}")
def get_trust_history(subject: str, limit: int = 20):
    events = [e.dict() for e in trust_events if e.subject == subject]
    return events[-limit:]

@app.get("/reputation/leaderboard")
def get_leaderboard(top: int = 20):
    ranked = sorted(reputation_scores.values(), key=lambda r: r.score, reverse=True)
    return [r.dict() for r in ranked[:top]]

# === Example Run: uvicorn src.reputation.reputation_engine:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("reputation.reputation_engine:app", host="0.0.0.0", port=8014, reload=True)
