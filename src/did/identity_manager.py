import os
import json
import base64
import hashlib
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from jwcrypto import jwk, jws

# === DID Utilities ===

def generate_ed25519_keypair() -> (bytes, bytes):
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    return priv_bytes, pub_bytes

def did_from_pubkey(pubkey: bytes) -> str:
    # DID example: did:picoin:<base58-encoded-pubkey>
    return "did:picoin:" + base64.urlsafe_b64encode(pubkey).decode('utf-8').rstrip("=")

# === DID Document Construction ===

def create_did_document(did: str, pubkey: bytes) -> Dict[str, Any]:
    return {
        "@context": "https://www.w3.org/ns/did/v1",
        "id": did,
        "verificationMethod": [{
            "id": f"{did}#key-1",
            "type": "Ed25519VerificationKey2018",
            "controller": did,
            "publicKeyBase64": base64.b64encode(pubkey).decode('utf-8')
        }],
        "authentication": [f"{did}#key-1"],
        "assertionMethod": [f"{did}#key-1"],
    }

# === Verifiable Credential Creation & Verification ===

def sign_credential(credential: Dict[str, Any], privkey: bytes) -> str:
    key = jwk.JWK.generate(kty='OKP', crv='Ed25519')
    key.import_from_bytes(privkey)
    payload = json.dumps(credential).encode()
    signer = jws.JWS(payload)
    signer.add_signature(key, None, json_encode({"alg": "EdDSA"}))
    return signer.serialize()

def verify_credential(signed_credential: str, pubkey: bytes) -> Optional[Dict[str, Any]]:
    key = jwk.JWK.generate(kty='OKP', crv='Ed25519')
    key.import_from_bytes(pubkey, is_private=False)
    try:
        verifier = jws.JWS()
        verifier.deserialize(signed_credential)
        verifier.verify(key)
        return json.loads(verifier.payload)
    except Exception as e:
        print("Verification failed:", str(e))
        return None

# === Selective Disclosure Utility ===

def selective_disclose(vc: Dict[str, Any], fields: list) -> Dict[str, Any]:
    """Return only selected fields from a verifiable credential."""
    return {k: v for k, v in vc.items() if k in fields}

# === Example Usage ===

if __name__ == "__main__":
    print("PiConsensus Decentralized Identity Demo")
    # Generate DID and DID Document
    priv, pub = generate_ed25519_keypair()
    did = did_from_pubkey(pub)
    doc = create_did_document(did, pub)
    print("DID Document:", json.dumps(doc, indent=2))

    # Issue a verifiable credential (KYC)
    credential = {
        "@context": ["https://www.w3.org/2018/credentials/v1"],
        "type": ["VerifiableCredential", "KYC"],
        "issuer": did,
        "issuanceDate": "2025-06-30T12:00:00Z",
        "credentialSubject": {
            "id": did,
            "name": "Alice",
            "age": 25,
            "jurisdiction": "US",
            "kycStatus": "verified"
        }
    }
    # Sign credential
    # NOTE: This is a stub for Ed25519 signature, actual JWS signing requires more handling
    # For production, use a library like didkit or identity-py for full credential flow
    signed_vc = base64.b64encode(json.dumps(credential).encode()).decode()
    print("Verifiable Credential (signed):", signed_vc)

    # Selective disclosure (e.g., prove only age)
    disclosed = selective_disclose(credential["credentialSubject"], ["age", "jurisdiction"])
    print("Selective Disclosure Example:", disclosed)
