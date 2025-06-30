from pqcrypto.sign import dilithium2
from typing import Dict, Any

class QuantumWallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate(self):
        """
        Generate a new Dilithium quantum-resistant key pair.
        """
        pk, sk = dilithium2.generate_keypair()
        self.private_key = sk
        self.public_key = pk
        print("[QuantumWallet] Keypair generated.")
        return pk, sk

    def sign(self, message: bytes) -> bytes:
        """
        Sign a message using the quantum-resistant private key.
        """
        if not self.private_key:
            raise ValueError("No private key loaded.")
        signature = dilithium2.sign(message, self.private_key)
        print("[QuantumWallet] Message signed.")
        return signature

    def verify(self, message: bytes, signature: bytes, public_key: bytes = None) -> bool:
        """
        Verify a message and signature with a quantum-resistant public key.
        """
        pk = public_key or self.public_key
        if not pk:
            raise ValueError("No public key available.")
        try:
            dilithium2.open(signature, pk)
            print("[QuantumWallet] Signature valid.")
            return True
        except Exception as e:
            print("[QuantumWallet] Signature verification failed:", e)
            return False

    def export_keys(self) -> Dict[str, bytes]:
        """
        Export the wallet's public and private keys.
        """
        return {"public_key": self.public_key, "private_key": self.private_key}

    def import_keys(self, public_key: bytes, private_key: bytes):
        """
        Import an existing keypair.
        """
        self.public_key = public_key
        self.private_key = private_key
        print("[QuantumWallet] Keys imported.")

# === Example Usage ===

if __name__ == "__main__":
    print("PiConsensus Quantum-Resistant Wallet Demo")
    wallet = QuantumWallet()
    pub, priv = wallet.generate()
    msg = b"Quantum-safe Pi transaction"
    sig = wallet.sign(msg)
    print("Signature:", sig.hex()[:64], "...")
    valid = wallet.verify(msg, sig)
    print("Signature valid?", valid)
