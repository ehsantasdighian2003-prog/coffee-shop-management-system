from app.core.unit_of_work import UnitOfWork
from app.core.security import (
    pwd_context,
    verify_password,
    create_access_token,
)
from app.core.exceptions import (
    UsernameAlreadyExistsException,
    AuthenticationException,
)

from app.repositories.auth_repository import AuthRepository


class AuthService:

    def __init__(self):
        self.repo = AuthRepository()

    # =========================
    # REGISTER
    # =========================

    def register(self, user_data):

        with UnitOfWork() as uow:

            existing_user = self.repo.get_user_by_username(
                uow.conn,
                user_data.username
            )

            if existing_user:
                raise UsernameAlreadyExistsException()

            hashed_password = pwd_context.hash(
                user_data.password
            )

            user = self.repo.create_user(
                conn=uow.conn,
                username=user_data.username,
                password=hashed_password,
                first_name=getattr(user_data, "first_name", None),
                last_name=getattr(user_data, "last_name", None),
                email=getattr(user_data, "email", None),
                phone_number=getattr(user_data, "phone_number", None),
                profile_image=getattr(user_data, "profile_image", None),
            )

            return {
                "message": "User registered successfully.",
                "user_id": user["id"],
            }

    # =========================
    # LOGIN
    # =========================

    def login(self, user_data):

        with UnitOfWork() as uow:

            user = self.repo.get_user_by_username(
                uow.conn,
                user_data.username
            )

            if not user:
                raise AuthenticationException(
                    "Invalid username or password"
                )

            if not user.get("is_active", True):
                raise AuthenticationException(
                    "User account is inactive"
                )

            if not verify_password(
                user_data.password,
                user["password"]
            ):
                raise AuthenticationException(
                    "Invalid username or password"
                )

            if hasattr(self.repo, "update_last_login"):
                self.repo.update_last_login(
                    uow.conn,
                    user["id"]
                )

            access_token = create_access_token(
                {
                    "user_id": user["id"]
                }
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
            }