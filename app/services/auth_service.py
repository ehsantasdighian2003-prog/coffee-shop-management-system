from typing import Any

from app.core.exceptions import (
    AuthenticationException,
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.core.unit_of_work import UnitOfWork
from app.schemas.auth import UserLogin, UserRegister


class AuthService:
    """
    Handles authentication and authorization business logic.
    """

    # ==================================================
    # REGISTER
    # ==================================================

    def register(
        self,
        user_data: UserRegister,
    ) -> dict[str, Any]:

        with UnitOfWork() as uow:

            existing_user = uow.auth.get_user_by_username(
                user_data.username
            )

            if existing_user:
                raise UsernameAlreadyExistsException()

            if user_data.email:

                existing_email = uow.auth.get_user_by_email(
                    user_data.email
                )

                if existing_email:
                    raise EmailAlreadyExistsException()

            hashed_password = hash_password(
                user_data.password
            )

            user = uow.auth.create_user(
                username=user_data.username,
                password=hashed_password,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                email=user_data.email,
                phone_number=user_data.phone_number,
                profile_image=user_data.profile_image,
            )

            return {
                "message": "User registered successfully.",
                "user_id": user["id"],
            }

    # ==================================================
    # LOGIN
    # ==================================================

    def login(
        self,
        user_data: UserLogin,
    ) -> dict[str, Any]:

        with UnitOfWork() as uow:

            user = uow.auth.get_user_by_username(
                user_data.username
            )

            if not user:

                raise AuthenticationException(
                    "Invalid username or password"
                )

            if not user["is_active"]:

                raise AuthenticationException(
                    "User account is inactive"
                )

            if not verify_password(
                user_data.password,
                user["password"],
            ):

                raise AuthenticationException(
                    "Invalid username or password"
                )

            uow.auth.update_last_login(
                user["id"]
            )

            payload = {
                "user_id": user["id"],
            }

            access_token = create_access_token(
                payload
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
            }