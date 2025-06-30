import time
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="PiConsensus Governance Proposal Marketplace", version="1.0")

# === Data Models ===

class Proposal(BaseModel):
    id: int
    title: str
    description: str
    proposer: str
    status: str = "open"  # open, closed, passed, rejected
    created_at: float = time.time()
    votes_for: int = 0
    votes_against: int = 0
    voters: List[str] = []

class Vote(BaseModel):
    proposal_id: int
    voter: str
    support: bool  # True = For, False = Against

# === In-memory Store (replace with DB in production) ===

proposals: Dict[int, Proposal] = {}
proposal_counter = 1

# === API Endpoints ===

@app.post("/governance/propose")
def submit_proposal(title: str, description: str, proposer: str):
    global proposal_counter
    proposal = Proposal(
        id=proposal_counter,
        title=title,
        description=description,
        proposer=proposer
    )
    proposals[proposal_counter] = proposal
    proposal_counter += 1
    return {"status": "submitted", "proposal_id": proposal.id}

@app.get("/governance/proposals")
def list_proposals(status: Optional[str] = None):
    result = [p for p in proposals.values() if (status is None or p.status == status)]
    return [p.dict() for p in result]

@app.get("/governance/proposal/{proposal_id}")
def get_proposal(proposal_id: int):
    proposal = proposals.get(proposal_id)
    if not proposal:
        raise HTTPException(404, "Proposal not found")
    return proposal.dict()

@app.post("/governance/vote")
def vote_on_proposal(vote: Vote):
    proposal = proposals.get(vote.proposal_id)
    if not proposal:
        raise HTTPException(404, "Proposal not found")
    if proposal.status != "open":
        raise HTTPException(400, "Voting is closed for this proposal")
    if vote.voter in proposal.voters:
        raise HTTPException(400, "Voter has already voted")
    if vote.support:
        proposal.votes_for += 1
    else:
        proposal.votes_against += 1
    proposal.voters.append(vote.voter)
    return {"status": "vote_recorded", "votes_for": proposal.votes_for, "votes_against": proposal.votes_against}

@app.post("/governance/close/{proposal_id}")
def close_proposal(proposal_id: int):
    proposal = proposals.get(proposal_id)
    if not proposal:
        raise HTTPException(404, "Proposal not found")
    if proposal.status != "open":
        raise HTTPException(400, "Proposal not open")
    proposal.status = "closed"
    # Simple majority rule for demo
    if proposal.votes_for > proposal.votes_against:
        proposal.status = "passed"
    else:
        proposal.status = "rejected"
    return {"status": proposal.status, "votes_for": proposal.votes_for, "votes_against": proposal.votes_against}

# === Example Run: uvicorn src.governance.proposal_marketplace:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("governance.proposal_marketplace:app", host="0.0.0.0", port=8008, reload=True)
