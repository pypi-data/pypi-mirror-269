import hashlib
import secrets


def generate_api_key(length=32) -> str:
    return "mydev-" + secrets.token_urlsafe(length)


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()
