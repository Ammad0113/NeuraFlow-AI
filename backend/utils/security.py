import hmac
import hashlib
import base64
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from backend.config.settings import settings

def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def _b64_decode(data: str) -> bytes:
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return hmac.compare_digest(sha, hashed_password)

def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())})

    header = {"alg": "HS256", "typ": "JWT"}
    header_bytes = json.dumps(header, separators=(',', ':')).encode('utf-8')
    payload_bytes = json.dumps(to_encode, separators=(',', ':')).encode('utf-8')

    segments = [
        _b64_encode(header_bytes),
        _b64_encode(payload_bytes)
    ]
    signing_input = ".".join(segments).encode('utf-8')
    signature = hmac.new(settings.SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
    segments.append(_b64_encode(signature))

    return ".".join(segments)

def decode_access_token(token: str) -> Optional[dict]:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        signing_input = f"{parts[0]}.{parts[1]}".encode('utf-8')
        signature = _b64_decode(parts[2])

        expected_sig = hmac.new(settings.SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected_sig):
            return None

        payload_bytes = _b64_decode(parts[1])
        payload = json.loads(payload_bytes.decode('utf-8'))

        if "exp" in payload and datetime.utcnow().timestamp() > payload["exp"]:
            return None

        return payload
    except Exception:
        return None
