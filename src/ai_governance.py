import os
import json
import datetime
from typing import List, Dict, Any, Optional
import requests
from transformers import pipeline

# === AI Models Initialization ===

# Sentiment analysis using HuggingFace Transformers
try:
    sentiment_analyzer = pipeline("sentiment-analysis")
except Exception:
    sentiment_analyzer = None  # In production, handle fallback or load a local model

# === Proposal Structures ===

class Proposal:
    def __init__(self, proposal_id: int, title: str, description: str, submitter: str, timestamp: Optional[str] = None):
        self.proposal_id = proposal_id
        self.title = title
        self.description = description
        self.submitter = submitter
        self.timestamp = timestamp or datetime.datetime.utcnow().isoformat()
        self.score = 0.0
        self.sentiment = "neutral"
        self.status = "pending"

    def to_dict(self):
        return {
            "proposal_id": self.proposal_id,
            "title": self.title,
            "description": self.description,
            "submitter": self.submitter,
            "timestamp": self.timestamp,
            "score": self.score,
            "sentiment": self.sentiment,
            "status": self.status
        }

# === AI Governance Core Functions ===

class AIGovernanceEngine:
    def __init__(self):
        self.proposals: Dict[int, Proposal] = {}
        self.next_id = 1

    def submit_proposal(self, title: str, description: str, submitter: str) -> Proposal:
        proposal = Proposal(self.next_id, title, description, submitter)
        proposal.sentiment = self.analyze_sentiment(proposal.description)
        proposal.score = self.score_proposal(proposal)
        self.proposals[self.next_id] = proposal
        self.next_id += 1
        return proposal

    def analyze_sentiment(self, text: str) -> str:
        if sentiment_analyzer is None:
            return "unknown"
        try:
            result = sentiment_analyzer(text[:512])[0]  # Truncate for performance
            return result['label'].lower()
        except Exception:
            return "error"

    def score_proposal(self, proposal: Proposal) -> float:
        # Example scoring: combine sentiment, length, keywords, and external signals
        score = 0.0
        if proposal.sentiment == "positive":
            score += 0.4
        elif proposal.sentiment == "neutral":
            score += 0.2
        if len(proposal.description) > 200:
            score += 0.2
        keywords = ["decentralized", "security", "scalable", "inclusive", "innovation"]
        for kw in keywords:
            if kw in proposal.description.lower():
                score += 0.08
        # External: Social sentiment (optional)
        score += self.external_social_sentiment(proposal.title) * 0.1
        return min(score, 1.0)

    def external_social_sentiment(self, topic: str) -> float:
        """
        Fetch and aggregate sentiment from external sources (e.g., Twitter, Reddit).
        This is a placeholder. Connect to real APIs in production.
        """
        # TODO: Integrate Twitter, Reddit, etc.
        return 0.5  # Neutral baseline

    def get_proposal(self, proposal_id: int) -> Optional[Proposal]:
        return self.proposals.get(proposal_id)

    def list_proposals(self) -> List[Dict[str, Any]]:
        return [p.to_dict() for p in self.proposals.values()]

    def approve_proposal(self, proposal_id: int) -> bool:
        proposal = self.get_proposal(proposal_id)
        if proposal:
            proposal.status = "approved"
            return True
        return False

    def reject_proposal(self, proposal_id: int) -> bool:
        proposal = self.get_proposal(proposal_id)
        if proposal:
            proposal.status = "rejected"
            return True
        return False

    def auto_decide(self, proposal_id: int) -> str:
        """
        Use AI scoring to make auto-approval/rejection.
        """
        proposal = self.get_proposal(proposal_id)
        if not proposal:
            return "not found"
        if proposal.score >= 0.7:
            proposal.status = "approved"
        elif proposal.score <= 0.3:
            proposal.status = "rejected"
        else:
            proposal.status = "pending"
        return proposal.status

# === Example: Integration with FastAPI or other frameworks ===

engine = AIGovernanceEngine()

if __name__ == "__main__":
    # Demo: CLI usage
    print("PiConsensus AI Governance Engine")
    while True:
        cmd = input("Command (submit/list/approve/reject/auto/exit): ").strip().lower()
        if cmd == "submit":
            title = input("Title: ")
            desc = input("Description: ")
            submitter = input("Submitter: ")
            prop = engine.submit_proposal(title, desc, submitter)
            print("Submitted:", prop.to_dict())
        elif cmd == "list":
            for p in engine.list_proposals():
                print(p)
        elif cmd == "approve":
            pid = int(input("Proposal ID: "))
            print("Approved:", engine.approve_proposal(pid))
        elif cmd == "reject":
            pid = int(input("Proposal ID: "))
            print("Rejected:", engine.reject_proposal(pid))
        elif cmd == "auto":
            pid = int(input("Proposal ID: "))
            status = engine.auto_decide(pid)
            print("Auto-decision:", status)
        elif cmd == "exit":
            break
        else:
            print("Unknown command.")
