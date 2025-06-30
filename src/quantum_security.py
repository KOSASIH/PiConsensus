from typing import Tuple, Dict, Any
from Crypto.Hash import SHA512
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

try:
    from pqcrypto.sign import dilithium2
except ImportError:
    dilithium2 = None  # Ensure pqcrypto is installed for full PQC support

# === Quantum-Safe Key Generation ===

def generate_ecc_keypair() -> Tuple[bytes, bytes]:
    """Generate ECDSA secp256k1 keypair (classic)."""
    key = ECC.generate(curve='P-256')
    private_key = key.export_key(format='DER')
    public_key = key.public_key().export_key(format='DER')
    return private_key, public_key

def generate_pqc_keypair() -> Tuple[bytes, bytes]:
    """Generate Dilithium2 quantum-resistant keypair."""
    if not dilithium2:
        raise RuntimeError("pqcrypto not installed.")
    pk, sk = dilithium2.generate_keypair()
    return sk, pk

def hybrid_keypair() -> Dict[str, Any]:
    """Generate a hybrid keypair (ECDSA + Dilithium2)."""
    ecc_priv, ecc_pub = generate_ecc_keypair()
    pqc_priv, pqc_pub = generate_pqc_keypair()
    return {
        "ecdsa_private": ecc_priv,
        "ecdsa_public": ecc_pub,
        "dilithium_private": pqc_priv,
        "dilithium_public": pqc_pub,
    }

# === Digital Signatures (Hybrid) ===

def ecdsa_sign(message: bytes, private_key: bytes) -> bytes    return signer.sign(h)

def ecdsa_verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
    """Verify ECDSA signature."""
    key = ECC.import_key(public_key)
    h = SHA512.new(message)
    verifier = DSS.new(key, 'fips-186-3')
    try:
        verifier.verify(h, signature)
        return True
    except ValueError:
        return False

def pqc_sign(message: bytes, private_key: bytes) -> bytes:
    """Sign message with Dilithium2 (quantum-safe)."""
    if not dilithium2:
        raise RuntimeError("pqcrypto not installed.")
    return dilithium2.sign(message, private_key)

def pqc_verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
    """Verify Dilithium2 signature."""
    if not dilithium2:
        raise RuntimeError("pqcrypto not installed.")
    try:
        dilithium2.open(signature, public_key)
        return True
    except Exception:
        return False

def hybrid_sign(message: bytes, hybrid_priv: Dict[str, bytes]) -> Dict[str, bytes]:
    """Produce a hybrid (ECDSA + Dilithium2) signature."""
    return {
        "ecdsa": ecdsa_sign(message, hybrid_priv["ecdsa_private"]),
        "pqc": pqc_sign(message, hybrid_priv["dilithium_private"]),
    }

def hybrid_verify(message: bytes, signature: Dict[str, bytes], hybrid_pub: Dict[str, bytes]) -> bool:
    """Verify hybrid signature (accepts only if both are valid)."""
    ecdsa_ok = ecdsa_verify(message, signature["ecdsa"], hybrid_pub["ecdsa_public"])
    pqc_ok = pqc_verify(message, signature["pqc"], hybrid_pub["dilithium_public"])
    return ecdsa_ok and pqc_ok

# === Key Migration & Utilities ===

def migrate_keys_to_pqc(ecc_private_key: bytes) -> Dict[str, Any]:
    """
    Assist migration from legacy ECDSA to hybrid quantum-resistant keys.
    """
    pqc_priv, pqc_pub = generate_pqc_keypair()
    return {
        "old_ecdsa_private": ecc_private_key,
        "new_dilithium_private": pqc_priv,
        "new_dilithium_public": pqc_pub,
    }

# === Example Usage ===

if __name__ == "__main__":
    print("Generating quantum-safe hybrid wallet...")
    keys = hybrid_keypair()
    msg = b"Ultra high-tech PiConsensus transaction"
    sig = hybrid_sign(msg, keys)
    print("Signature valid?", hybrid_verify(msg, sig, keys))
    print("Legacy to PQC migration example:", migrate_keys_to_pqc(keys["ecdsa_private"]))
