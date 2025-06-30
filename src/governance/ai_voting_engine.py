import time
import threading
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from sklearn.ensemble import IsolationForest

app = FastAPI(title="PiConsensus AI-Driven Governance Engine", version="1.0")

# === Data Models ===

class Proposal(BaseModel):
    id: int
    title: str
    description: str
    creator: str
    start_time: float
    end_time: float
    votes: Dict[str, float] = {}  # voter: votes (quadratic)
    status: str = "open"  # open/closed

class Vote(BaseModel):
    proposal_id: int
    voter: str
    amount: float  # Number of tokens used for voting

# === Governance State ===

proposals: Dict[int, Proposal] = {}
proposal_counter = 0
votes_log: List[Dict[str, Any]] = []

# === AI/ML Voting Pattern Analysis (Fraud/Anomaly Detection) ===

class VoteAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(n_estimators=50, contamination=0.05)
        self.trained = False

 v in votes])
        self.model.fit(X)
        self.trained = True

    def check(self, votes: List[Vote]) -> List[str]:
        if not self.trained or not votes:
            return []
        X = np.array([[v.amount] for v in votes])
        preds = self.model.predict(X)
        anomalies = [votes[i].voter for i in range(len(votes)) if preds[i] == -1]
        return anomalies

vote_analyzer = VoteAnomalyDetector()

# === Quadratic Voting Utility ===

def quadratic_vote(amount: float) -> float:
    return np.sqrt(amount)

# === Proposal Management ===

@app.post("/propose")
def create_proposal(title: str, description: str, creator: str, duration_sec: int = 3600):
    global proposal_counter
    proposal_id = proposal_counter
    proposal = Proposal(
        id=proposal_id,
        title=title,
        description=description,
        creator=creator,
        start_time=time.time(),
        end_time=time.time() + duration_sec,
    )
    proposals[proposal_id] = proposal
    proposal_counter += 1
    return {"proposal_id": proposal_id, "status": "created"}

@app.get("/proposals")
def list_proposals():
    return [p.dict() for p in proposals.values()]

@app.post("/vote")
def cast_vote(vote: Vote):
    if vote.proposal_id not in proposals:
        raise HTTPException(404, "Proposal not found")
    proposal =}

@app.get("/proposals/{proposal_id}/result")
def proposal_result(proposal_id: int):
    if proposal_id not in proposals:
        raise HTTPException(404, "Proposal not found")
    proposal = proposals[proposal_id]
    total_votes = sum(proposal.votes.values())
    return {
        "proposal_id": proposal_id,
        "title": proposal.title,
        "total_votes": total_votes,
        "votes": proposal.votes,
        "status": proposal.status,
    }

@app.post("/analyze_votes/{proposal_id}")
def analyze_votes(proposal_id: int):
    if proposal_id not in proposals:
        raise HTTPException(404, "Proposal not found")
    votes = [Vote(proposal_id=proposal_id, voter=v, amount=(proposals[proposal_id].votes[v])**2) for v in proposals[proposal_id].votes]
    vote_analyzer.fit(votes)
    anomalies = vote_analyzer.check(votes)
    return {"anomalous_voters": anomalies}

# === Background Proposal Closer ===

def proposal_closer():
    while True:
        now = time.time()
        for p in proposals.values():
            if p.status == "open" and now > p.end_time:
                p.status = "closed"
        time.sleep(10)

threading.Thread(target=proposal_closer, daemon=True).start()

# === Example Run: uvicorn src.governance.ai_voting_engine:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("governance.ai_voting_engine:app", host="0.0.0.0", port=8001, reload=True)
