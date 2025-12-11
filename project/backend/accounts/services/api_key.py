import hashlib
import secrets


def generate_key(prefix_length: int = 16) -> tuple[str, str, str]:
    """
    Generate a new API key.

    Returns (full_key, prefix, hashed_key).
    """
    raw_key = secrets.token_urlsafe(48)
    prefix = raw_key[:prefix_length]
    hashed = hash_key(raw_key)
    return raw_key, prefix, hashed


def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

