from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64

# Hashing a password
def hash_password(password: str) -> (str, str):
    """
    Hash a password using PBKDF2.
    Returns the base64-encoded hash and the salt used.
    """
    password_bytes = password.encode('utf-8')  # Convert to bytes
    salt = os.urandom(16)  # Generate a random salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    key = kdf.derive(password_bytes)  # Derive the password hash
    return base64.b64encode(key).decode('utf-8'), base64.b64encode(salt).decode('utf-8')

# Verifying a password
def verify_password(stored_hash: str, stored_salt: str, provided_password: str) -> bool:
    """
    Verify the provided password matches the stored hash and salt.
    """
    password_bytes = provided_password.encode('utf-8')  # Convert to bytes
    salt = base64.b64decode(stored_salt)  # Decode the stored salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    try:
        kdf.verify(password_bytes, base64.b64decode(stored_hash))  # Verify the password
        return True
    except Exception:
        return False
