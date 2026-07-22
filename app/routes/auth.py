from fastapi import APIRouter, status

from app.schemas.auth import (
    RegisterResponse,
    Token,
    UserLogin,
    UserRegister,
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth_service = AuthService()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse,
    summary="Register a new user",
    description="Create a new user account.",
)
def register(
    user: UserRegister,
) -> RegisterResponse:
    """
    Register a new user.
    """
    return auth_service.register(user)


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user",
    description="Authenticate a user and return a JWT access token.",
)
def login(
    user: UserLogin,
) -> Token:
    """
    Authenticate a user.
    """
    return auth_service.login(user)
