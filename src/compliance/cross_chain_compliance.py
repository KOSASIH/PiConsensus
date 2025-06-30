import os
import requests
from web3 import Web3
from typing import List, Dict, Any

# === Example Chain RPC URLs (customize for your needs) ===
CHAIN_CONFIG = {
    "ethereum": os.environ.get("ETH_RPC_URL", "https://mainnet.infura.io/v3/YOUR_KEY"),
    "bsc": os.environ.get("BSC_RPC_URL", "https://bsc-dataseed.binance.org/"),
    "polygon": os.environ.get("POLY_RPC_URL", "https://polygon-rpc.com/"),
}

# === Example Compliance Rules ===
BLACKLISTED_ADDRESSES = set([
    "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
    # Add more
])

MAX_TX_AMOUNT = 1_000_000  # Example: 1,000,000 Pi (adjust as needed)

def is_blacklisted(address: str) -> bool:
    return address.lower() in BLACKLISTED_ADDRESSES

def exceeds_amount(amount: int) -> bool:
    return amount > MAX_TX_AMOUNT

def check_kyc(address: str) -> bool:
    # Example: Query an external KYC service (stub)
    # In production, replace with real KYC API or on-chain attestation check
    resp = requests.get(f"https://kyc.pi.example/api/v1/check/{address}")
    if resp.status_code == 200:
        return resp.json().get("kyc_passed", False)
    return False

# === Cross-Chain Connector ===

class ChainConnector:
    def __init__(self, chain_name: str, rpc_url: str):
        self.chain_name = chain_name
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.web3.is_connected():
            raise RuntimeError(f"Could not connect to {chain_name} node.")

    def get_latest_transactions(self, address: str, limit=10) -> List[Dict[str, Any]]:
        # This is a stub; use chain-specific indexers (Etherscan, BSCScan, etc.) for production
        # Here, just returns empty for demo
        return []

# === Compliance Engine ===

class CrossChainComplianceEngine:
    def __init__(self, chain_config: Dict[str, str]):
        self.connectors = {name: ChainConnector(name, url) for name, url in chain_config.items()}

    def check_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        """
        tx = {
            "from": "0x...",
            "to": "0x...",
            "value": 12345,
            "chain": "ethereum"
        }
        """
        compliance = {
            "blacklisted": is_blacklisted(tx["from"]) or is_blacklisted(tx["to"]),
            "exceeds_amount": exceeds_amount(tx["value"]),
            "kyc_sender": check_kyc(tx["from"]),
            "kyc_receiver": check_kyc(tx["to"]),
        }
        compliance["compliant"] = all([
            not compliance["blacklisted"],
            not compliance["exceeds_amount"],
            compliance["kyc_sender"],
            compliance["kyc_receiver"],
        ])
        return compliance

    def monitor_address_across_chains(self, address: str) -> Dict[str, Any]:
        results = {}
        for chain, connector in self.connectors.items():
            txs = connector.get_latest_transactions(address)
            results[chain] = [self.check_transaction(tx) for tx in txs]
        return results

    def report(self, tx: Dict[str, Any], compliance: Dict[str, Any]):
        # Send report to admin dashboard, SIEM system, or compliance officer
        print(f"[Compliance] TX {tx} | Compliance: {compliance}")

# === Example Usage ===

if __name__ == "__main__":
    print("PiConsensus Automated Cross-Chain Compliance Layer Demo")
    engine = CrossChainComplianceEngine(CHAIN_CONFIG)
    # Simulate a transaction for testing
    test_tx = {
        "from": "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
        "to": "0x1234567890abcdef1234567890abcdef12345678",
        "value": 123_456,
        "chain": "ethereum"
    }
    compliance = engine.check_transaction(test_tx)
    engine.report(test_tx, compliance)
