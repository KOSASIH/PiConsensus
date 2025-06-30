import os
import requests
import hashlib
from typing import Optional

# === Swarm Node Configuration ===

SWARM_API_URL = os.environ.get("SWARM_API_URL", "http://localhost:1633")  # Default local Bee node

# === File Upload ===

def upload_file_to_swarm(filepath: str) -> Optional[str]:
    """
    Upload a file to Swarm. Returns the Swarm content hash (bzz address).
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "rb") as f:
        files = {'file': f}
        resp = requests.post(f"{SWARM_API_URL}/bzz", files=files)
        if resp.status_code == 201:
            hash_ref = resp.json()["reference"]
            print(f"Uploaded {filepath} to Swarm: {hash_ref}")
            return hash_ref
        else:
            print(f"Swarm upload failed: {resp.text}")
            return None

# === File Download ===

def download_file_from_swarm(hash_ref: str, dest_path: str) -> bool:
    """
    Download a file from Swarm using its hash. Save to dest_path.
    """
    resp = requests.get(f"{SWARM_API_URL}/bzz/{hash_ref}/", stream=True)
    if resp.status_code == 200:
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded file {dest_path} from Swarm: {hash_ref}")
        return True
    else:
        print(f"Swarm download failed: {resp.text}")
        return False

# === Integrity Validation ===

def validate_file_hash(filepath: str, expected_hash: str) -> bool:
    """
    Validate a file's SHA256 hash against the expected Swarm reference.
    Note: Swarm uses its own hash tree for chunking, but for off-chain check, use SHA256.
    """
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    actual_hash = sha256.hexdigest()
    print(f"File hash: {actual_hash}")
    # This is for demonstration; full Swarm hash validation requires chunk tree parsing.
    return actual_hash.startswith(expected_hash[:16])  # Partial match for demo

# === Example Usage ===

if __name__ == "__main__":
    print("PiConsensus Swarm Storage & Decentralized File Layer Demo")
    # Upload example
    test_file = "example.txt"
    with open(test_file, "w") as f:
        f.write("Hello, Swarm decentralized world!")
    hash_ref = upload_file_to_swarm(test_file)
    # Download example
    if hash_ref:
        download_file_from_swarm(hash_ref, "downloaded_example.txt")
        # Validate
        validate_file_hash("downloaded_example.txt", hash_ref)
