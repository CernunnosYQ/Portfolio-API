from jwt import encode, exceptions, decode
from typing import Optional
from datetime import datetime, timedelta

from core.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    token = encode(
        payload={**data, "exp": expire},
        key=settings.SECRET_KEY,
        algorithm=(settings.ALGORITHM),
    )
    return token.encode("UTF-8")


def validate_access_token(token):
    try:
        decoded_token = decode(
            token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return {"success": True, "payload": decoded_token}
    except exceptions.DecodeError:
        detail = "Invalid token"
    except exceptions.ExpiredSignatureError:
        detail = "Token expired"
    return {"success": False, "detail": detail}
