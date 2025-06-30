import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from src import constants
from utils import helpers
from incident_response import team

app = FastAPI(
    title="PiConsensus: Decentralized Quantum-Resistant Stable Coin Ecosystem API",
    version="2.0.0",
    description="Feature-rich API and dashboard backend for PiConsensus"
)

# CORS for frontend dashboard integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Blockchain API Models
class MintRequest(BaseModel):
    address: str
    amount: float

class BurnRequest(BaseModel):
    address: str
    amount: float

class VoteRequest(BaseModel):
    address: str
    amount: float

class IncidentReport(BaseModel):
    reporter: str
    description: str

# Dummy blockchain interaction functions (replace with web3.py logic)
def mint_tokens(address: str, amount: float) -> str:
    # TODO: Real blockchain call
    return f"Minted {amount} tokens to {address}"

def burn_tokens(address: str, amount: float) -> str:
    return f"Burned {amount} tokens from {address}"

def cast_vote(address: str, amount: float) -> str:
    return f"Vote cast by {address} for {amount}"

# Dashboard root
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h1>PiConsensus API & Dashboard</h1>
    <p>Welcome to the PiConsensus backend.</p>
    <ul>
      <li><a href='/docs'>Swagger API docs</a></li>
      <li><a href='/status'>Network Status</a></li>
    </ul>
    """

# Network status endpoint
@app.get("/status")
def status():
    return {
        "network": "online",
        "pi_coin_symbol": constants.PI_COIN_SYMBOL,
        "supply": constants.PI_COIN_SUPPLY,
        "block_time": constants.PI_COIN_BLOCK_TIME,
        "mining_difficulty": constants.PI_COIN_MINING_DIFFICULTY
    }

# Blockchain operations
@app.post("/mint")
def api_mint(req: MintRequest):
    result = mint_tokens(req.address, req.amount)
    return {"result": result}

@app.post("/burn")
def api_burn(req: BurnRequest):
    result = burn_tokens(req.address, req.amount)
    return {".isupper()}

# IPFS & Ethereum utilities
@app.post("/pin_ipfs/")
def pin_file(file_path: str):
    hash = helpers.pin_file_to_ipfs(file_path)
    return {"ipfs_hash": hash}

@app.get("/ethereum/block_number")
def get_block_number():
    return {"block_number": helpers.get_ethereum_block_number()}

# Incident response integration
team_config = {"members": ["admin@pi.org", "security@pi.org"]}
incident_team = team.Team(team_config)

@app.post("/incident/report")
def report_incident(report: IncidentReport):
    incident_id = len(incident_team.incidents) + 1
    incident = {"id": incident_id, "reporter": report.reporter, "description": report.description}
    incident_team.assign_to_incident(incident)
    return {"incident_id": incident_id, "status": "assigned"}

@app.get("/incident/{incident_id}")
def get_incident(incident_id: int):
    incident = incident_team.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

# Admin interface
@app.post("/admin/update_constants")
def update_constants(key: str, value: Any):
    if not hasattr(constants, key):
        raise HTTPException(status_code=404, detail="Constant not found")
    setattr(constants, key, value)
    return {"status": "updated", "key": key, "new_value": value}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)