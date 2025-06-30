import time
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="PiConsensus Decentralized Oracle Engine", version="1.0")

# === Data Models ===

class OracleSource(BaseModel):
    id: int
    name: str
    url: str  # API endpoint to fetch data from
    data_key: str  # Key in the JSON response to extract
    description: Optional[str] = None
    active: bool = True
    registered_at: float = time.time()

class OracleFeed(BaseModel):
    id: int
    source_id: int
    value: Any
    timestamp: float = time.time()

# === In-memory Store (replace with DB in production) ===

oracle_sources: Dict[int, OracleSource] = {}
oracle_feeds: List[OracleFeed] = []
source_counter = 1
feed_counter = 1

# === API Endpoints ===

@app.post("/oracle/register")
def register_oracle(name: str, url: str, data_key: str, description: Optional[str] = None):
    global source_counter
    source = OracleSource(
        id=source_counter,
        name=name,
        url=url,
        data_key=data_key,
        description=description
    )
    oracle_sources[source_counter] = source
    source_counter += 1
    return {"status": "registered", "oracle": source.dict()}

@app.get("/oracle/sources")
def list_oracle_sources(active: Optional[bool] = None):
    sources = [s.dict() for s in oracle_sources.values() if (active is None or s.active == active)]
    return sources

@app.post("/oracle/fetch/{source_id}")
def fetch_from_oracle(source_id: int):
    global feed_counter
    source = oracle_sources.get(source_id)
    if not source or not source.active:
        raise HTTPException(404, "Oracle source not found or inactive")
    try:
        resp = httpx.get(source.url, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
        value = data.get(source.data_key)
        if value "source_id": source_id}

# === Example Run: uvicorn src.oracle.oracle_engine:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("oracle.oracle_engine:app", host="0.0.0.0", port=8013, reload=True)
