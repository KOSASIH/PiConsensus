import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import ipfshttpclient

app = FastAPI(title="PiConsensus Decentralized Storage/Archival Engine", version="1.0")

# === Connect to IPFS Node ===

try:
    ipfs = ipfshttpclient.connect()  # Defaults to /dns/localhost/tcp/5001/http
except Exception as e:
    ipfs = None
    print("[DecentralizedStorage] Warning: Could not connect to IPFS node:", e)

# === API Models ===

class PinRequest(BaseModel):
    cid: str

# === API Endpoints ===

@app.post("/storage/upload")
async def upload_file(file: UploadFile = File(...)):
    if not ipfs:
        raise HTTPException(500, "IPFS node not connected")
    contents = await file.read()
    result = ipfs.add_bytes(contents)
    ipfs.pin.add(result)
    return {"cid": result, "filename": file.filename}

@app.get("/storage/retrieve/{cid}")
def retrieve_file(cid: str):
    if not ipfs:
        raise HTTPException(500, "IPFS node not connected")
    try:
        data = ipfs.cat(cid)
        return {"cid": cid, "data": data.decode(errors="replace")}
    except Exception as e:
        raise HTTPException(404, f"Could not retrieve CID {cid}: {e}")

@app.post("/storage/pin")
def pin_content(req: PinRequest):
    if not ipfs:
        raise HTTPException(500, "IPFS node not connected")
    try:
        ipfs.pin.add(req.cid)
        return {"status": "pinned", "cid": req.cid}
    except Exception as e:
        raise HTTPException(400}")

@app.get("/storage/pins")
def list_pins():
    if not ipfs:
        raise HTTPException(500, "IPFS node not:
        raise HTTPException(400, f"Could not list pins: {e}")

# === Example Run: uvicorn src.storage.decentralized_storage:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("storage.decentralized_storage:app", host="0.0.0.0", port=8006, reload=True)
