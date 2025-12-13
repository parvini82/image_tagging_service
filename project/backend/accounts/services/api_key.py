import secrets
import hashlib
from accounts.models import APIKey, User


def hash_key(raw_key: str) -> str:
    """Hash an API key using SHA256."""
    return hashlib.sha256(raw_key.encode()).hexdigest()


def generate_api_key(user: User) -> tuple[str, APIKey]:
    """
    Generate a new API key for a user.
    
    Returns:
        (raw_key, api_key_object): The raw key (shown once) and the stored object
    """
    # Check if user already has an API key
    if APIKey.objects.filter(user=user).exists():
        raise ValueError("User already has an API key. Revoke the existing one first.")
    
    # Generate random key: fk_live_<16 random chars>
    random_part = secrets.token_urlsafe(12)[:16]
    raw_key = f"fk_live_{random_part}"
    
    # Store only hashed key + prefix
    prefix = raw_key[:16]
    hashed_key = hash_key(raw_key)
    
    api_key = APIKey.objects.create(
        user=user,
        key=hashed_key,
        prefix=prefix,
    )
    
    return raw_key, api_key
