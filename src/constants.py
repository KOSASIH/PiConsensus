import os
from typing import List, Dict

def env(key: str, default):
    """Fetch value from environment, or use default if not set. Supports type safety."""
    value = os.environ.get(key)
    if value is None:
        return default
    if isinstance(default, bool):
        return value.lower() in ("1", "true", "yes")
    if isinstance(default, int):
        return int(value)
    if isinstance(default, float):
        return float(value)
    if isinstance(default, list):
        return value.split(',')
    return value

# ==================== PI COIN CORE PARAMETERS ====================

PI_COIN_SYMBOL: str = env("PI_COIN_SYMBOL", "Pi")
PI_COIN_NAME: str = env("PI_COIN_NAME", "Pi Coin")
PI_COIN_VALUE: int = env("PI_COIN_VALUE", 314_159)  # Pi Coin value in USD (three hundred fourteen thousand one hundred fifty-nine)
PI_COIN_SUPPLY: int = env("PI_COIN_SUPPLY", 100_000_000_000)
PI_COIN_DECIMALS: int = env("PI_COIN_DECIMALS", 18)
PI_COIN_TRANSACTION_FEE: float = env("PI_COIN_TRANSACTION_FEE", 0.01)
PI_COIN_MAX_TRANSACTION_SIZE: int = env("PI_COIN_MAX_TRANSACTION_SIZE", 1_000_000)
PI_COIN_MINIMUM_BALANCE: int = env("PI_COIN_MINIMUM_BALANCE", 1)

# ==================== NETWORK AND BLOCKCHAIN PARAMETERS ====================

PI_COIN_BLOCK_TIME: int = env("PI_COIN_BLOCK_TIME", 10)  # seconds
PI_COIN_MINING_DIFFICULTY: int = env("PI_COIN_MINING_DIFFICULTY", 1000)
PI_COIN_MINING_REWARD: float = env("PI_COIN_MINING_REWARD", 12.5)
PI_COIN_NETWORK_PROTOCOL: str = env("PI_COIN_NETWORK_PROTOCOL", "PoS")  # Proof of Stake
PI_COIN_GENESIS_BLOCK_TIMESTAMP: str = env("PI_COIN_GENESIS_BLOCK_TIMESTAMP", "2025-01-01T00:00:00Z")

# ==================== GOVERNANCE & COMPLIANCE ====================

PI_COIN_GOVERNANCE_MODEL: str = env("PI_COIN_GOVERNANCE_MODEL", "Decentralized")
PI_COIN_KYC_REQUIRED: bool = env("PI_COIN_KYC_REQUIRED", True)
PI_COIN_COMPLIANCE_JURISDICTIONS: List[str] = env("PI_COIN_COMPLIANCE_JURISDICTIONS", ["US", "EU", "UK", "SG", "JP", "AU"])
PI_COIN_COMPLIANCE_LEVEL: str = env("PI_COIN_COMPLIANCE_LEVEL", "Ultra-Strict, Real-Time, Multi-Jurisdictional")

# ==================== SECURITY & CRYPTOGRAPHY ====================

PI_COIN_ENCRYPTION_ALGORITHM: str = env("PI_COIN_ENCRYPTION_ALGORITHM", "AES-256-GCM")
PI_COIN_HASHING_ALGORITHM: str = env("PI_COIN_HASHING_ALGORITHM", "SHA-512")
PI_COIN_SIGNATURE_SCHEME: str = env("PI_COIN_SIGNATURE_SCHEME", "ECDSA-secp256k1")
PI_COIN_MULTISIG_ENABLED: bool = env("PI_COIN_MULTISIG_ENABLED", True)
PI_COIN_SMART_CONTRACT_AUDIT_PROVIDER: str = env("PI_COIN_AUDIT_PROVIDER", "Quantstamp, OpenZeppelin, Trail of Bits")

# ==================== STAKING & REWARDS ====================

PI_COIN_MIN_STAKE_AMOUNT: int = env("PI_COIN_MIN_STAKE_AMOUNT", 100)
PI_COIN_STAKE_REWARD_RATE: float = env("PI_COIN_STAKE_REWARD_RATE", 0.05)  # 5% annual
PI_COIN_MAX_STAKE_DURATION_DAYS: int = env("PI_COIN_MAX_STAKE_DURATION_DAYS", 3650)  # 10 years

# ==================== API & INFRASTRUCTURE ====================

PI_COIN_API_REQUEST_LIMIT: int = env("PI_COIN_API_REQUEST_LIMIT", 10_000)  # per hour
PI_COIN_API_KEY_EXPIRATION: int = env("PI_COIN_API_KEY_EXPIRATION", 86_400)  # 24 hours
PI_COIN_MAX_PEERS: int = env("PI_COIN_MAX_PEERS", 10_000)
PI_COIN_NODE_TIMEOUT: int = env("PI_COIN_NODE_TIMEOUT", 10)
PI_COIN_CONNECTION_RETRY_INTERVAL: int = env("PI_COIN_CONNECTION_RETRY_INTERVAL", 3)

# ==================== ADVANCED/EXPANDABLE SETTINGS ====================

PI_COIN_AI_GOVERNANCE_ENABLED: bool = env("PI_COIN_AI_GOVERNANCE_ENABLED", True)
PI_COIN_QUANTUM_RESISTANT: bool = env("PI_COIN_QUANTUM_RESISTANT", True)
PI_COIN_DEFI_INTEGRATION: bool = env("PI_COIN_DEFI_INTEGRATION", True)
PI_COIN_LAYER_2_ENABLED: bool = env("PI_COIN_LAYER_2_ENABLED", True)
PI_COIN_AUDIT_TRAIL_ENABLED: bool = env("PI_COIN_AUDIT_TRAIL_ENABLED", True)

# ==================== DYNAMIC/UTILITY FUNCTIONS ====================

def is_jurisdiction_compliant(country_code: str) -> bool:
    """
    Check if a given country code is supported for compliance.
    """
    return country_code.upper() in [c.upper() for c in PI_COIN_COMPLIANCE_JURISDICTIONS]

def describe():
    """
    Print a human-readable summary of Pi Coin configuration.
    """
    return {
        "Symbol": PI_COIN_SYMBOL,
        "Name": PI_COIN_NAME,
        "Value (USD)": PI_COIN_VALUE,
        "Supply": PI_COIN_SUPPLY,
        "Decimals": PI_COIN_DECIMALS,
        "Governance": PI_COIN_GOVERNANCE_MODEL,
        "KYC": PI_COIN_KYC_REQUIRED,
        "Quantum Resistant": PI_COIN_QUANTUM_RESISTANT,
        "AI Governance": PI_COIN_AI_GOVERNANCE_ENABLED,
        "Staking Rate": PI_COIN_STAKE_REWARD_RATE,
        "Jurisdictions": PI_COIN_COMPLIANCE_JURISDICTIONS,
    }

# ==================== END OF FILE ====================
