from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from user_agents import parse as parse_ua
import redis
import time
import hashlib

app = FastAPI(title="PiConsensus API Gateway", version="1.0")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
rdb = redis.Redis(host="localhost", port=6379, db=0)

# === Abuse & Anomaly Detection Utilities ===

def is_suspicious_user_agent(user_agent: str) -> bool:
    ua = parse_ua(user_agent)
    if not ua.is_bot and ua.browser.family not in ["", "Unknown"]:
        return False
    return True

def is_ip_flagged(ip: str) -> bool:
    return rdb.get(f"bad_ip:{ip}") is not None

def flag_ip(ip: str, reason: str = "abuse"):
    rdb.setex(f"bad_ip:{ip}", 3600, reason)

def adaptive_rate_limit(ip: str) -> str:
    """Increase rate limits for trusted, decrease for flagged."""
    if is_ip_flagged(ip):
        return "10/minute"
    # Could enhance with scoring based on API key, reputation, etc.
    return "100/minute"

def log_anomaly(ip: str, reason: str, details: dict):
    key = f"anomaly:{hashlib.sha256((ip + str(time.time())).encode()).hexdigest()}"
    rdb.setex(key, 3600, str({"ip": ip, "reason": reason, "details": details}))

# === API Gateway Routes ===

@app.middleware("http")
async def abuse_detection_middleware(request: Request, call_next):
    ip = get_remote_address(request)
    user_agent = request.headers.get("User-Agent", "")
    if is_suspicious_user_agent(user_agent):
        flag_ip(ip, "bot or suspicious user agent")
        log_anomaly(ip, "suspicious_user_agent", {"user_agent": user_agent})
        return JSONResponse(status_code=403, content={"error": "Access denied: Suspicious user agent"})
    if is_ip_flagged(ip):
        return JSONResponse(status_code=429, content={"error": "Your IP is temporarily blocked due to suspicious activity."})
    response = await call_next(request)
    return response

@app.get("/status")
@limiter.limit("50/minute")
async def status():
    return {"status": "OK", "message": "PiConsensus API Gateway operational."}

@app.post("/api/v1/tx")
@limiter.limit("20/minute")
async def submit_tx(request: Request):
    ip = get_remote_address(request)
    body = await request.json()
    # Basic abuse logic: e.g., block repeated identical payloads
    tx_hash = hashlib.sha256(str(body).encode()).hexdigest()
    if rdb.get(f"recent_tx:{ip}:{tx_hash}"):
        flag_ip(ip, "replay attack")
        log_anomaly(ip, "replay_attack", {"tx_hash": tx_hash, "body": body})
        raise HTTPException(status_code=429, detail="Repeated transaction detected.")
    rdb.setex(f"recent_tx:{ip}:{tx_hash}", 60, 1)
    # Forward transaction to backend here
    return {"status": "submitted", "tx_hash": tx_hash}

@app.get("/api/v1/analytics")
@limiter.limit("10/minute")
async def analytics():
    # Example endpoint for querying analytics
    return {"analytics": "Not implemented"}

# === Example of Adaptive Rate Limit Endpoint ===

@app.get("/api/v1/profile")
async def profile(request: Request):
    ip = get_remote_address(request)
    limit = adaptive_rate_limit(ip)
    # Manually apply limiter for custom rate limit
    if not limiter.hit(limit, request):
        raise HTTPException(status_code=429, detail="Rate limit reached.")
    return {"profile": "Your profile info here"}

# === Run with: uvicorn src.api_gateway.gateway:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_gateway.gateway:app", host="0.0.0.0", port=8000, reload=True)
