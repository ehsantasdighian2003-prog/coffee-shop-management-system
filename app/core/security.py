from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import (
    AuthenticationException,
    PermissionDeniedException,
)
from app.core.unit_of_work import UnitOfWork


# ==================================================
# PASSWORD HASHING
# ==================================================

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify plain password against hashed password.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def hash_password(
    password: str,
) -> str:
    """
    Hash password using Argon2.
    """

    return pwd_context.hash(
        password,
    )


# ==================================================
# JWT CONFIGURATION
# ==================================================

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)


security = HTTPBearer(
    auto_error=False
)


# ==================================================
# CREATE ACCESS TOKEN
# ==================================================

def create_access_token(
    data: dict,
) -> str:
    """
    Create JWT access token.
    """

    payload = data.copy()

    expire = datetime.now(
        timezone.utc,
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    payload.update(
        {
            "exp": expire,
        }
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ==================================================
# CURRENT USER
# ==================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> Dict[str, Any]:
    """
    Validate JWT token and return current user.
    """

    if credentials is None:
        raise AuthenticationException(
            "Authentication credentials were not provided."
        )

    try:
        token = credentials.credentials

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("user_id")

        if not user_id:
            raise AuthenticationException(
                "Invalid token"
            )

        with UnitOfWork() as uow:
            user = uow.users.get_by_id(user_id)

        if not user:
            raise AuthenticationException(
                "User not found"
            )

        if not user["is_active"]:
            raise AuthenticationException(
                "User account is inactive"
            )

        return user

    except JWTError:
        raise AuthenticationException(
            "Invalid token"
        )


# ==================================================
# ROLE CHECK
# ==================================================

def admin_required(
    user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Allow access only for admin users.
    """

    if user["role"] != "admin":
        raise PermissionDeniedException()

    return user