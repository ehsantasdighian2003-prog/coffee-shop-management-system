from datetime import (
    datetime,
    timedelta,
    timezone
)

from fastapi import (
    Depends,
    HTTPException,
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from jose import (
    jwt,
    JWTError
)

from passlib.context import CryptContext

from app.core.config import settings
from app.core.database import get_connection

from app.repositories.user_repository import UserRepository

from app.core.exceptions import AuthenticationException


# =========================
# PASSWORD HASHING
# =========================

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def hash_password(
    password: str
) -> str:

    return pwd_context.hash(password)


# =========================
# JWT CONFIG
# =========================

SECRET_KEY = settings.JWT_SECRET_KEY

ALGORITHM = settings.JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)

security = HTTPBearer()


# =========================
# CREATE ACCESS TOKEN
# =========================

def create_access_token(
    data: dict
) -> str:

    payload = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================
# GET CURRENT USER
# =========================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    try:

        token = credentials.credentials

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if not user_id:
            raise AuthenticationException(
                "Invalid token"
            )

        conn = get_connection()

        try:

            repo = UserRepository()

            user = repo.get_by_id(
                conn,
                user_id
            )

        finally:

            conn.close()

        if not user:
            raise AuthenticationException(
                "User not found"
            )

        return user

    except JWTError:

        raise AuthenticationException(
            "Invalid token"
        )


# =========================
# ADMIN CHECK
# =========================

def admin_required(
    user=Depends(get_current_user)
):

    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin only access"
        )

    return user