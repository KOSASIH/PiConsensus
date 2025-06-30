import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import didkit

app = FastAPI(title="PiConsensus DID Management & Verifiable Credentials", version="1.0")

# === API Models ===

class KeyRequest(BaseModel):
    key_type: str = "ed25519"  # ed25519, secp256k1, etc.

class IssueVCRequest(BaseModel):
    did: str
    subject: dict
    credential_type: str = "VerifiableCredential"
    issuer: str
    proof_purpose: str = "assertionMethod"
    verification_method: str

class VerifyVCRequest(BaseModel):
    vc: dict

# === DID & Key Management ===

@app.post("/did/key")
def generate_did_key(req: KeyRequest):
    key = didkit.generate_ed25519_key() if req.key_type == "ed25519" else didkit.generate_secp256k1_key()
    did = didkit.key_to_did("key", key)
    vm = didkit.key_to_verification_method("key", key)
    return {"did": did, "key": key, "verification_method": vm}

@app.get("/did/resolve/{did}")
def resolve_did(did: str):
    try:
        doc = didkit.resolve_did(did, '{}')
        return json.loads(doc)
    except Exception as e:
        raise HTTPException(400, f"Could not resolve DID: {e}")

VCs) ===

@app.post("/vc/issue")
def issue_vc(req: IssueVCRequest):
    vc = {
        "@context": ["https://www.w3.org/2018/credentials/v1"],
        "type": [req.credential_type],
        "issuer": req.issuer,
        "issuanceDate": didkit.get_iso_datetime(),
        "credentialSubject": req.subject,
    }
    options = {
        "proofPurpose": req.proof_purpose,
        "verificationMethod": req.verification_method,
    }
    try:
        signed_vc = didkit.issue_credential(json.dumps(vc), json.dumps(options), req.key)
        return json.loads(signed_vc)
    except Exception as e:
        raise HTTPException(400, f"Could not issue VC: {e}")

@app.post("/vc/verify")
def verify_vc(req: VerifyVCRequest):
    try:
        options = {}
        result = didkit.verify_credential(json.dumps(req.vc), json.dumps(options))
        return json.loads(result)
    except Exception as e:
        raise HTTPException(400, f"Could not verify VC: {e}")

# === Example Run: uvicorn src.identity.did_management:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("identity.did_management:app", host="0.0.0.0", port=8007, reload=True)
