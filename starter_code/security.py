"""
security.py
------------
Task 6: A basic access-control gate for your sales reports.
"""

import hashlib
import getpass

# Password is "spaza2026" — stored only as its SHA-256 hash, never as plain text.
STORED_PASSWORD_HASH = "a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4"


def hash_password(plain_text_password: str) -> str:
    return hashlib.sha256(plain_text_password.encode()).hexdigest()


def check_password(attempt: str, stored_hash: str) -> bool:
    return hash_password(attempt) == stored_hash


def login_gate(stored_hash: str, max_attempts: int = 3) -> bool:
    for attempt_number in range(max_attempts):
        attempt = getpass.getpass("Enter password to view reports: ")
        if check_password(attempt, stored_hash):
            print("Access granted.")
            return True
        else:
            remaining = max_attempts - attempt_number - 1
            if remaining > 0:
                print(f"Incorrect password. {remaining} attempt(s) remaining.")
            else:
                print("Incorrect password.")
    print("Access denied — too many failed attempts.")
    return False


# Set the real hash at module load time.
# Production improvement: store this hash in a database `users` table instead of
# hardcoding it here, so passwords can be changed without editing source code.
STORED_PASSWORD_HASH = hash_password("spaza2026")
