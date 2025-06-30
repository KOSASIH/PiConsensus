import time
import json
import random
import threading
from typing import List, Dict, Any, Callable, Optional
import numpy as np
import requests

# === Oracle Provider Interface ===

class OracleProvider:
    def __init__(self, name: str, url: str, parse_fn: Callable[[Any], float], weight: float = 1.0):
        self.name = name
        self.url = url
        self.parse_fn = parse_fn
        self.weight = weight
        self.last_value = None
        self.last_timestamp = None

    def fetch(self) -> Optional[float]:
        try:
            resp = requests.get(self.url, timeout=5)
            value = self.parse_fn(resp)
            self.last_value = value
            self.last_timestamp = time.time()
            return value
        except Exception as e:
            print(f"[OracleProvider] {self.name} fetch failed: {e}")
            return None

# === Example Oracle Providers (e.g., for price feeds) ===

def parse_coingecko(resp):
    data = resp.json()
    return data["pi"]["usd"]

def parse_binance(resp):
    data = resp.json()
    return float(data["price"])

ORACLE_PROVIDERS = [
    OracleProvider("CoinGecko", "https://api.coingecko.com/api/v3/simple/price?ids=pi&vs_currencies=usd", parse_coingecko, weight=1.0),
    OracleProvider("Binance", "https://api.binance.com/api/v3/ticker/price?symbol=PIUSDT", parse_binance, weight=1.1),
    # Add more providers as needed
]

# === Data Aggregator ===

class OracleAggregator:
    def __init__(self, providers: List[OracleProvider]):
        self.providers = providers

    def fetch_all(self) -> Dict[str, float]:
        results = {}
        for provider in self.providers:
            value = provider.fetch()
            if value is not None:
                results[provider.name] = value
        return results

    def aggregate(self, values: Dict[str, float]) -> float:
        """
        Aggregate values using weighted median for robustness.
        """
        if not values:
            raise ValueError("No values to aggregate.")
        weights = [p.weight for p in self.providers if p.name in values]
        vals = [values[p.name] for p in self.providers if p.name in values]
        weighted_vals = np.repeat(vals, [int(w * 100) for w in weights])
        median = float(np.median(weighted_vals))
        return median

    def score_providers(self, values: Dict[str, float], agg_value: float) -> Dict[str, float]:
        """
        Score providers based on proximity to aggregate value.
        """
        scores = {}
        for name, value in values.items():
            scores[name] = 1.0 / (1 + abs(value - agg_value))
        return scores

    def resolve_dispute(self, values: Dict[str, float]) -> str:
        """
        Resolve disputes by picking the value closest to the median.
        """
        agg_value = self.aggregate(values)
        closest = min(values.items(), key=lambda x: abs(x[1] - agg_value))
        return f"Dispute resolved: {closest[0]} value ({closest[1]}) accepted."

    def run_once(self) -> Dict[str, Any]:
        """
        Fetch, aggregate, score, and resolve in one pass.
        """
        values = self.fetch_all()
        if not values:
            return {"error": "No oracle data available."}
        agg = self.aggregate(values)
        scores = self.score_providers(values, agg)
        dispute = self.resolve_dispute(values) if len(values) > 1 and max(values.values()) - min(values.values()) > 0.05 * agg else "No dispute."
        result = {
            "oracle_values": values,
            "aggregated": agg,
            "provider_scores": scores,
            "dispute_resolution": dispute
        }
        print(json.dumps(result, indent=2))
        return result

    def run_continuous(self, poll_interval=60):
        """
        Continuously aggregate oracle data and output results.
        """
        def loop():
            while True:
                self.run_once()
                time.sleep(poll_interval)
        threading.Thread(target=loop, daemon=True).start()

# === Example Usage ===

if __name__ == "__main__":
    aggregator = OracleAggregator(ORACLE_PROVIDERS)
    print("Decentralized Oracle Aggregator Demo")
    aggregator.run_once()
    # To enable continuous mode, uncomment:
    # aggregator.run_continuous(poll_interval=60)
    # while True: time.sleep(60)
