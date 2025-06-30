import time
import random
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="PiConsensus Privacy-Preserving Analytics Engine", version="1.0")

# === Data Models ===

class AnalyticsEvent(BaseModel):
    event_type: str
    value: float
    timestamp: float = time.time()
    group: Optional[str] = None  # e.g., region, client type

class InsightQuery(BaseModel):
    event_type: str
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    group: Optional[str] = None
    noisy: Optional[bool] = False  # If True, adds random noise for privacy

# === In-Memory Store (replace with secure DB in production) ===

analytics_events: List[AnalyticsEvent] = []

# === Privacy-Aware Aggregation ===

def aggregate_events(event_type: str, start_time=None, end_time=None, group=None) -> List[float]:
    """Filter and aggregate event values."""
    filtered = [
        e.value
        for e in analytics_events
        if e.event_type == event_type
        and (start_time is None or e.timestamp >= start_time)
        and (end_time is None or e.timestamp <= end_time)
        and (group is None or e.group == group)
    ]
    return filtered

def add_noise(val: float, scale: float = 1.0) -> float:
    """Simple Laplacian noise mechanism for DP-like effect."""
    return valightQuery):
    data = aggregate_events(query.event_type, query.start_time, query.end_time, query.group)
    count = len(data)
    if count == 0:
        return {"msg": "No data for query"}
    avg = float(np.mean(data))
    min_v = float(np.min(data))
    max_v = float(np.max(data))
    sum_v = float(np.sum(data))
    if query.noisy:
        # Add noise to aggregated values for privacy
        avg = add_noise(avg, scale=1.0)
        min_v = add_noise(min_v, scale=1.0)
        max_v = add_noise(max_v, scale=1.0)
        sum_v = add_noise(sum_v, scale=2.0)
    return {
        "event_type": query.event_type,
        "group": query.group,
        "count": count,
        "avg": avg,
        "min": min_v,
        "max": max_v,
        "sum": sum_v,
        "noisy": query.noisy,
    }

@app.get("/analytics/events")
def list_events(limit: int = 50):
    return [e.dict() for e in analytics_events[-limit:]]

# === Example Run: uvicorn src.analytics.privacy_analytics:app --reload ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("analytics.privacy_analytics:app", host="0.0.0.0", port=8011, reload=True)
