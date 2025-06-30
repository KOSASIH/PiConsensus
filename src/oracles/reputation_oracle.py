import time
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="PiConsensus Decentralized Reputation Oracle", version="1.0")

# === Data Model ===

class ReputationFeedback(BaseModel):
    subject: str      # address/agent/contract being rated
    rater: str        # address/agent submitting feedback
    score: float      # -1.0 (very bad) to 1.0 (excellent)
    timestamp: float = time.time()
    comment: str = ""

class ReputationScore(BaseModel):
    subject: str
    score: float
    n_feedback: int
    last_update: float

# === In-memory Store (replace with DB/distributed store in production) ===

feedbacks: List[ReputationFeedback] = []
scores: Dict[str, ReputationScore] = {}

# === Aggregation Algorithm (pluggable) ===

def compute_score(subject: str) -> ReputationScore:
    """Weighted average with recency bias."""
    relevant = [f for f in feedbacks if f.subject == subject]
    if not relevant:
        return ReputationScore(subject=subject, score=0.0, n_feedback=0, last_update=time.time())
    scores_arr = np.array([f.score for f in relevant])
    times = np.array([f.timestamp for f in relevant])
    # Recency weighting: more recent feedback is weighted higher
    weights = np.exp((times - times.min()) / (60*60*24*7))  # 1 week scale
    weighted_score = float(np.average(scores_arr, weights=weights))
    return ReputationScore(
        subject=subject,
        score=weighted_score,
        n_feedback=len(relevant),
        last_update=times.max()
    )

def update_score(subject: str):
    scores[subject] = compute_score(subject)

# === REST API ===

@app.post("/feedback")
def submit_feedback(fb: ReputationFeedback):
    if abs(fb.score) > 1.0:
        raise HTTPException(400, "Score must be between -1.0 and 1.0")
    feedbacks.append(fb)
    update_score(fb.subject)
    return {"msg": "Feedback submitted", "subject": fb.subject}

@app.get("/score/{subject}")
def get_score(subject: str):
    if subject not in scores:
        update_score(subject)
    return scores.get(subject).dict()

@app.get("/feedback/{subject}")
def get_feedback(subject: str):
    relevant = [f.dict() for f in feedbacks if f.subject == subject]
    return {"subject": subject, "feedback": relevant}

@app.get("/top/{n}")
def top_subjects(n: int = 10):
    sorted_scores = sorted(scores.values(), key=lambda s: s.score, reverse=True)
    return [s.dict() for s in sorted_scores[:n]]

# === Example Run: uvicorn src.oracles.reputation_oracle:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("oracles.reputation_oracle:app", host="0.0.0.0", port=8003, reload=True)
