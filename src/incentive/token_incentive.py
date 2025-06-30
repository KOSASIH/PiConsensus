import time
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="PiConsensus Tokenized Incentive Layer & Reward Engine", version="1.0")

# === Data Models ===

class RewardRule(BaseModel):
    id: int
    activity: str  # e.g., "validate", "propose", "bridge", "contribute"
    reward_amount: float
    asset: str = "Pi"
    active: bool = True

class RewardEvent(BaseModel):
    id: int
    rule_id: int
    recipient: str
    activity: str
    amount: float
    asset: str
    timestamp: float = time.time()
    details: Optional[Dict[str, Any]] = None

# === In-memory Store (replace with DB/smart contract in prod) ===

reward_rules: Dict[int, RewardRule] = {}
reward_events: List[RewardEvent] = []
rule_counter = 1
event_counter = 1

# === API Endpoints ===

@app.post("/incentive/rule")
def create_rule(activity: str, reward_amount: float, asset: Optional[str] = "Pi"):
    global rule_counter
    rule = RewardRule(id=rule_counter, activity=activity, reward_amount=reward_amount, asset=asset)
    reward_rules[rule_counter] = rule
    rule_counter += 1
    return {"status": "rule_created", "rule": rule.dict()}

@app.get("/incentive/rules")
def list_rules(active: Optional[bool] = None):
    rules = [r.dict() for r in reward_rules.values() if (active is None or r.active == active)]
    return rules

@app.post("/incentive/reward")
def distribute_reward(rule_id: int, recipient: str, details: Optional[Dict[str, Any]] = None):
    global event_counter
    rule = reward_rules.get(rule_id)
    if not rule or not rule.active:
        raise HTTPException(400, "Invalid or inactive reward rule")
    event = RewardEvent(
        id=event_counter,
        rule_id=rule_id,
        recipient=recipient,
        activity=rule.activity,
        amount=rule.reward_amount,
        asset=rule.asset,
        timestamp=time.time(),
        details=details
    )
    reward_events disable_rule(rule_id: int):
    rule = reward_rules.get(rule_id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    rule.active = False
    return {"status": "disabled", "rule_id": rule_id}

# === Example Run: uvicorn src.incentive.token_incentive:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("incentive.token_incentive:app", host="0.0.0.0", port=8010, reload=True)
