import hashlib
import logging
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuantumResistanceUtility:
    def __init__(self):
        self.algorithms = {
            'RSA': self.is_rsa_quantum_resistant,
            'ECDSA': self.is_ecdsa_quantum_resistant,
            'SHA-256': self.is_sha256_quantum_resistant,
            # Add more algorithms as needed
        }

    def is_rsa_quantum_resistant(self, key_size):
        """Check if RSA is quantum resistant based on key size."""
        if key_size >= 3072:
            logger.info("RSA with key size %d is considered quantum resistant.", key_size)
            return True
        else:
            logger.warning("RSA with key size %d is NOT considered quantum resistant.", key_size)
            return False

    def is_ecdsa_quantum_resistant(self, curve_name):
        """Check if ECDSA is quantum resistant based on curve."""
        # Commonly used curves and their quantum resistance
        quantum_resistant_curves = ['P-256', 'P-384', 'P-521']
        if curve_name in quantum_resistant_curves:
            logger.info("ECDSA with curve %s is considered quantum resistant.", curve_name)
            return True
        else:
            logger.warning("ECDSA with curve %s is NOT considered quantum resistant.", curve_name)
            return False

    def is_sha256_quantum_resistant(self):
        """SHA-256 is not quantum resistant, but it's still widely used."""
        logger.warning("SHA-256 is NOT quantum resistant. Consider using SHA-3 or other alternatives.")
        return False

    def recommend_quantum_resistant_algorithms(self):
        """Provide recommendations for quantum-resistant algorithms."""
        recommendations = {
            'Post-Quantum Cryptography': [
                'Lattice-based cryptography (e.g., NTRU)',
                'Code-based cryptography (e.g., McEliece)',
                'Multivariate polynomial cryptography',
                'Hash-based signatures (e.g., XMSS)',
            ],
            'Quantum Key Distribution (QKD)': [
                'BB84 protocol',
                'E91 protocol',
            ]
        }
        logger.info("Recommendations for quantum-resistant algorithms:")
        for category, algos in recommendations.items():
            logger.info("%s: %s", category, ", ".join(algos))

    def generate_rsa_key_pair(self, key_size=3072):
        """Generate an RSA key pair."""
        if not self.is_rsa_quantum_resistant(key_size):
            raise ValueError("RSA key size is not quantum resistant.")
        
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def generate_ecdsa_key_pair(self, curve_name='P-256'):
        """Generate an ECDSA key pair."""
        if not self.is_ecdsa_quantum_resistant(curve_name):
            raise ValueError("ECDSA curve is not quantum resistant.")
        
        private_key = ec.generate_private_key(
            ec.SECP256R1() if curve_name == 'P-256' else ec.SECP384R1() if curve_name == 'P-384' else ec.SECP521R1()
        )
        public_key = private_key.public_key()
        return private_key, public_key

# Example usage
if __name__ == "__main__":
    utility = QuantumResistanceUtility()

    # Check RSA quantum resistance
    utility.is_rsa_quantum_resistant(3072)

    # Check ECDSA quantum resistance
    utility.is_ecdsa_quantum_resistant('P-256')

    # Check SHA-256 quantum resistance
    utility.is_sha256_quantum_resistant()

    # Recommend quantum-resistant algorithms
    utility.recommend_quantum_resistant_algorithms()

    # Generate RSA key pair
    try:
        rsa_private, rsa_public = utility.generate_rsa_key_pair(3072)
        logger.info("RSA Key Pair generated successfully.")
    except ValueError as e:
        logger.error("Error generating RSA key pair: %s", e)

    # Generate ECDSA key pair
    try:
        ecdsa_private, ecdsa_public = utility.generate_ecdsa_key_pair('P-256')
        logger.info("ECDSA Key Pair generated successfully.")
    except ValueError as e:
        logger.error("Error generating ECDSA key pair: %s", e)
