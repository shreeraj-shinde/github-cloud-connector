from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import get_settings


settings = get_settings()


class AuthService:

    def __init__(self, token: str):
        self.token = token

    def encrypt(self, token: str) -> str:
        payload = {
            "token": token,
            "exp": datetime.now(timezone.utc) + timedelta(hours=settings.TOKEN_EXPIRE_HOURS),
        }
        return jwt.encode(payload, settings.SECRET, algorithm=settings.ALGORITHM)

    def decrypt(self, token: str) -> str:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM])
        return payload.get("token")