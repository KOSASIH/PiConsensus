import time
from typing import Dict, Any, Callable, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="PiConsensus Autonomous Economic Agent API", version="1.0")

# === Agent Model ===

class Agent(BaseModel):
    id: str
    owner: str
    balance: float
    rules: Dict[str, Any]
    actions: List[str] = []
    last_action: Optional[float] = None

# === In-memory Agent Store ===

agents: Dict[str, Agent] = {}

# === Example Action Functions ===

def send_payment(agent: Agent, to: str, amount: float) -> str:
    if agent.balance < amount:
        return f"Insufficient balance for {agent.id}"
    agent.balance -= amount
    # Simulate sending: in production, integrate with blockchain
    return f"Agent {agent.id} sent {amount} Pi to {to}"

def auto_invest(agent: Agent, asset: str, threshold: float) -> str:
    # Simulate investment logic
    if agent.balance > threshold:
        agent.balance -= threshold
        return f"Agent {agent.id} invested {threshold} Pi in {asset}"
    return f"No investment: {agent.id} balance below threshold"

# === Rule Engine ===

ACTION_MAP: Dict[str, Callable] = {
    "send_payment": send_payment,
    "auto_invest": auto_invest,
}

def evaluate_rules(agent: Agent):
    # Simple rule evaluation engine (expand as needed)
    responses = []
    for rule_name, rule_params in agent.rules.items():
        action_func = ACTION_MAP.get(rule_name)
        if action_func:
            resp = action_func(agent, **rule_params)
            agent.actions.append(resp)
            responses.append(resp)
            agent.last_action = time.time()
    return responses

# === API Endpoints ===

@app.post("/agents/")
def create_agent(agent: Agent):
    if agent.id in agents:
        raise HTTPException(400, "Agent with this ID already exists")
    agents[agent.id] = agent
    return {"status": "created", "agent_id": agent.id}

@app.get("/agents/{agent_id}")
def get_agent(agent_id: str):
    agent = agents.get(agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    return agent.dict()

@app.post("/agents/{agent_id}/trigger")
def trigger_agent(agent_id: str):
    agent = agents.get(agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    responses = evaluate_rules(agent)
    return {"status": "triggered", "responses": responses}

@app.post("/agents/{agent_id}/deposit")
def deposit(agent_id: str, amount: float):
    agent = agents.get(agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    agent.balance += amount
    return {"status": "deposit_ok", "new_balance": agent.balance}

@app.get("/agents/")
def list_agents():
    return [a.dict() for a in agents.values()]

# === Scheduler for Autonomous Triggering ===

def schedule_all_agents():
    for agent in agents.values():
        evaluate_rules(agent)

scheduler = BackgroundScheduler()
scheduler.add_job(schedule_all_agents, 'interval', seconds=30)
scheduler.start()

# === Example Run: uvicorn src.agents.aea_api:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agents.aea_api:app", host="0.0.0.0", port=8002, reload=True)
