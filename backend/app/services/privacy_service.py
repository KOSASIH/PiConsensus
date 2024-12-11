import os
import base64
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PrivacyService:
    def __init__(self):
        self.secret_key = self.generate_secret_key()
        self.fernet = Fernet(self.secret_key)

    def generate_secret_key(self):
        """Generate a secure random key for encryption."""
        key = Fernet.generate_key()
        logger.info("Generated a new secret key.")
        return key

    def encrypt_data(self, data):
        """Encrypt the given data using Fernet symmetric encryption."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        encrypted_data = self.fernet.encrypt(data)
        logger.info("Data encrypted successfully.")
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        """Decrypt the given encrypted data using Fernet symmetric encryption."""
        decrypted_data = self.fernet.decrypt(encrypted_data)
        logger.info("Data decrypted successfully.")
        return decrypted_data.decode('utf-8')

    def anonymize_data(self, user_data):
        """Anonymize user data by hashing sensitive fields."""
        hashed_data = {}
        for key, value in user_data.items():
            if key in ['email', 'phone_number', 'ssn']:  # Sensitive fields
                hashed_value = self.hash_data(value)
                hashed_data[key] = hashed_value
            else:
                hashed_data[key] = value
        logger.info("User data anonymized successfully.")
        return hashed_data

    def hash_data(self, data):
        """Hash the given data using SHA-256."""
        hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hasher.update(data.encode('utf-8'))
        hashed_value = hasher.finalize()
        return base64.urlsafe_b64encode(hashed_value).decode('utf-8')

    def generate_rsa_key_pair(self):
        """Generate an RSA key pair for asymmetric encryption."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        logger.info("RSA key pair generated successfully.")
        return private_key, public_key

    def encrypt_with_rsa(self, public_key, data):
        """Encrypt data using the provided RSA public key."""
        encrypted_data = public_key.encrypt(
            data.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        logger.info("Data encrypted with RSA successfully.")
        return encrypted_data

    def decrypt_with_rsa(self, private_key, encrypted_data):
        """Decrypt data using the provided RSA private key."""
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        logger.info("Data decrypted with RSA successfully.")
        return decrypted_data.decode('utf-8')

# Example usage
if __name__ == "__main__":
    privacy_service = PrivacyService()

    # Encrypt and decrypt data
    sensitive_data = "This is a secret message."
    encrypted_data = privacy_service.encrypt_data(sensitive_data)
    decrypted_data = privacy_service.decrypt_data(encrypted_data)
    logger.info("Original Data: %s", sensitive_data)
    logger.info("Decrypted Data: %s", decrypted_data)

    # Anonymize user data
    user_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "phone_number": "123-456-7890",
        "ssn": "123-45-6789"
    }
    anonymized_data = privacy_service.anonymize_data(user_data)
    logger.info("Anonymized Data: %s", anonymized_data)

    # Generate RSA key pair
    private_key, public_key = privacy_service.generate_rsa_key_pair()

