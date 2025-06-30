import subprocess
import json
import os
from typing import Dict, Any
from Crypto.Random import get_random_bytes

CIRCUIT_PATH = "circuits/kyc_proof.circom"
BUILD_DIR = "circuits/build"
INPUT_JSON = os.path.join(BUILD_DIR, "input.json")
WITNESS_WTN = os.path.join(BUILD_DIR, "witness.wtns")
PROOF_JSON = os.path.join(BUILD_DIR, "proof.json")
PUBLIC_JSON = os.path.join(BUILD_DIR, "public.json")

# === Example Circom Circuit (KYC) ===
# pragma circom 2.0.0;
# template KYCProof() {
#   signal input secret_age;
#   signal public min_age;
#   signal output valid;
#   valid <== secret_age >= min_age;
# }
# component main = KYCProof();

def generate_input_json(secret_age: int, min_age: int):
    os.makedirs(BUILD_DIR, exist_ok=True)
    with open(INPUT_JSON, "w") as f:
        json.dump({"secret_age": secret_age, "min_age": min_age}, f)

def run_circom_and_snarkjs():
    # Compile the circuit
    subprocess.run(["circom", CIRCUIT_PATH, "--r1cs", "--wasm", "--sym", "-o", BUILD_DIR], check=True)
    # Generate the witness
    subprocess.run(["node", os.path.join(BUILD_DIR, "kyc_proof_js/generate_witness.js"),
                    os.path.join(BUILD_DIR, "kyc_proof_js/kyc_proof.wasm"),
                    INPUT_JSON,
                    WITNESS_WTN], check=True)
    # Setup (trusted setup phase, only once)
    subprocess.run(["snarkjs", "groth16", "setup",
                    os.path.join(BUILD_DIR, "kyc_proof.r1cs"),
                    "pot12_final.ptau",
                    os.path.join(BUILD_DIR, "kyc_proof_0000.zkey")], check=True)
    # Generate the proof
    subprocess.run(["snarkjs", "groth16", "prove",
                    os.path.join(BUILD_DIR, "kyc_proof_0000.zkey"),
                    WITNESS_WTN,
                    PROOF_JSON,
                    PUBLIC_JSON], check=True)

def verify_proof() -> bool:
    # Verify the proof
    result = subprocess.run(["snarkjs", "groth16", "verify",
                             os.path.join(BUILD_DIR, "verification_key.json"),
                             PUBLIC_JSON,
                             PROOF_JSON], capture_output=True, text=True)
    print(result.stdout)
    return "OK!" in result.stdout

# === Python API ===

def generate_kyc_proof(secret_age: int, min_age: int) -> Dict[str, Any]:
    """
    Generates a zk-SNARK proof that secret_age >= min_age without revealing the actual age.
    Returns the proof and public signals.
    """
    generate_input_json(secret_age, min_age)
    run_circom_and_snarkjs()
    with open(PROOF_JSON) as pf, open(PUBLIC_JSON) as pubf:
        proof = json.load(pf)
        public = json.load(pubf)
    return {"proof": proof, "public": public}

def verify_kyc_proof() -> bool:
    """
    Verifies the previously generated zk-SNARK proof.
    """
    return verify_proof()

# === Example Usage ===

if __name__ == "__main__":
    print("PiConsensus ZK Selective Disclosure Demo (KYC Age Proof)")
    # User wants to prove age >= 18, but does not reveal true age
    proof_obj = generate_kyc_proof(secret_age=24, min_age=18)
    print("Proof:", json.dumps(proof_obj["proof"], indent=2))
    print("Public signals:", proof_obj["public"])
    valid = verify_kyc_proof()
    print("Proof valid?", valid)
