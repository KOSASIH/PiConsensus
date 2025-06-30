import time
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pygroth

app = FastAPI(title="PiConsensus Zero-Knowledge Proof Service Layer", version="1.0")

# === Data Models ===

class ZKPRequest(BaseModel):
    statement: str  # e.g., 'x > 18'
    witness: Dict[str, Any]  # e.g., {"x": 21}

class ZKPVerifyRequest(BaseModel):
    vk: dict
    proof: dict
    public: dict

# === In-memory store for demo ===

proofs: Dict[str, dict] = {}
vks: Dict[str, dict] = {}
pk_cache: Optional[dict] = None  # You can persist keypairs for circuits

# === ZKP Demo Functions ===

def generate_keys(statement: str):
    # In a real system, you'd compile a circuit for the statement.
    # For demo: create keys for a trivial circuit.
    (pk, vk) = pygroth.keygen(pygroth.circuit_example())
    return pk, vk

@app.post("/zkp/generate")
def generate_zkp(req: ZKPRequest):
    global pk_cache
    # For demo, always use the same example circuit
    if pk_cache is None:
        pk, vk = generate_keys(req.statement)
        pk_cache = pk
        vks[req.statement] = vk
    else:
        pk = pk_cache
        vk = vks.get(req.statement)
    # The witness must satisfy the circuit
    try:
        proof = pygroth.prove(pk, pygroth.circuit_example(), req.witness)
        proof_id = f"proof-{int(time.time()*1000)}"
        proofs[proof_id] = {"proof": proof, "public": req.witness, "vk": vk, "statement": req.statement}
        return {"proof_id": proof_id, "proof": proof, "public": req.witness, "vk": vk, "statement": req.statement}
    except Exception as e:
        raise HTTPException(400, f"Could not generate proof: {e}")

@app.post("/zkp/verify")
def verify_zkp(req: ZKPVerifyRequest):
    try:
        valid = pygroth.verify(req.vk, pygroth.circuit_example(), req.proof, req.public)
        return {"valid": bool(valid)}
    except Exception as e:
        raise HTTPException(400, f"Verification failed: {e}")

@app.get("/zkp/proofs/{proof_id}")
def get_proof(proof_id: str == "__main__":
    import uvicorn
    uvicorn.run("zkp.zkp_service:app", host="0.0.0.0", port=8012, reload=True)
