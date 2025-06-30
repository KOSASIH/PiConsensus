import time
import threading
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Callable
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# === Simulated Blockchain Transaction Stream ===

def get_recent_transactions(n: int = 100) -> pd.DataFrame:
    """
    Simulate fetching the n most recent Pi Coin transactions.
    In production, connect to blockchain node or API.
    """
    np.random.seed(int(time.time()))
    # Random data: [amount, fee, block_time, sender_entropy, receiver_entropy]
    data = np.random.normal(loc=[314, 0.01, 10, 0.5, 0.5], scale=[50, 0.005, 2, 0.2, 0.2], size=(n, 5))
    df = pd.DataFrame(data, columns=["amount", "fee", "block_time", "sender_entropy", "receiver_entropy"])
    df["tx_hash"] = [f"0x{np.random.bytes(16).hex()}" for _ in range(n)]
    df["timestamp"] = pd.Timestamp.now()
    return df

# === Anomaly Detection Engine ===

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        self.scaler = StandardScaler()
        self.last_fit = None

    def fit(self, df: pd.DataFrame):
        X = df[["amount", "fee", "block_time", "sender_entropy", "receiver_entropy"]]
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.last_fit = pd.Timestamp.now()
        print(f"[AnomalyDetector] Model trained on {len(df)} transactions.")

    def predict(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        X = df[["amount", "fee", "block_time", "sender_entropy", "receiver_entropy"]]
        X_scaled = self.scaler.transform(X)
        preds = self.model.predict(X_scaled)
        anomalies = df[preds == -1]
        return anomalies.to_dict(orient="records")

    def stream_monitor(self, poll_interval: float = 5.0, callback: Callable = None):
        """
        Continuously monitor incoming blockchain transactions for anomalies.
        Calls callback(anomalies) if found.
        """
        def monitor():
            print("[AnomalyDetector] Starting live anomaly monitoring...")
            while True:
                txs = get_recent_transactions(50)
                if self.last_fit is None or (pd.Timestamp.now() - self.last_fit).seconds > 60:
                    self.fit(txs)
                anomalies = self.predict(txs)
                if anomalies and callback:
                    callback(anomalies)
                time.sleep(poll_interval)
        t = threading.Thread(target=monitor, daemon=True)
        t.start()

# === Alerting & Auto-Response ===

def alert_admin(anomalies: List[Dict[str, Any]]):
    """
    Alert admin or security team about detected anomalies.
    In production, send email, push notification, or on-chain event.
    """
    print("\n[ALERT] 🚨 Anomalies Detected 🚨")
    for a in anomalies:
        print(a)

# === Example Usage ===

if __name__ == "__main__":
    print("Demo: PiConsensus On-Chain Anomaly Detector")
    detector = AnomalyDetector()
    # Initial training on sample data
    txs = get_recent_transactions(200)
    detector.fit(txs)
    # Predict anomalies on new batch
    new_txs = get_recent_transactions(50)
    anomalies = detector.predict(new_txs)
    alert_admin(anomalies)
    # Start live monitoring (Ctrl+C to exit)
    detector.stream_monitor(callback=alert_admin)
    while True:
        time.sleep(60)
