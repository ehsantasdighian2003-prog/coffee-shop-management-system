from fastapi import APIRouter, status

from app.schemas.auth import (
    UserRegister,
    UserLogin,
    Token,
)

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth_service = AuthService()


# =========================
# REGISTER
# =========================
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(user: UserRegister):

    return auth_service.register(user)


# =========================
# LOGIN
# =========================
@router.post(
    "/login",
    response_model=Token,
)
def login(user: UserLogin):

    return auth_service.login(user)