from typing import Any

from app.core.unit_of_work import UnitOfWork
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.core.exceptions import (
    UsernameAlreadyExistsException,
    EmailAlreadyExistsException,
    AuthenticationException,
)


class AuthService:
    """
    Handles authentication and authorization business logic.
    """

    # ==================================================
    # REGISTER
    # ==================================================

    def register(
        self,
        user_data,
    ) -> dict[str, Any]:

        with UnitOfWork() as uow:

            # Check username

            existing_user = uow.auth.get_user_by_username(
                user_data.username
            )

            if existing_user:
                raise UsernameAlreadyExistsException()

            # Check email

            if user_data.email:

                existing_email = uow.auth.get_user_by_email(
                    user_data.email
                )

                if existing_email:
                    raise EmailAlreadyExistsException()

            # Hash password

            hashed_password = hash_password(
                user_data.password
            )

            # Create user

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
        user_data,
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