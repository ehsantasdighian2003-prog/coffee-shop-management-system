from typing import Any

from app.core.unit_of_work import UnitOfWork

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.core.exceptions import (
    UsernameAlreadyExistsException,
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

            existing_user = uow.auth.get_user_by_username(
                user_data.username
            )

            if existing_user:
                raise UsernameAlreadyExistsException()

            hashed_password = hash_password(
                user_data.password
            )

            user = uow.auth.create_user(
                username=user_data.username,
                password=hashed_password,
                first_name=getattr(
                    user_data,
                    "first_name",
                    None,
                ),
                last_name=getattr(
                    user_data,
                    "last_name",
                    None,
                ),
                email=getattr(
                    user_data,
                    "email",
                    None,
                ),
                phone_number=getattr(
                    user_data,
                    "phone_number",
                    None,
                ),
                profile_image=getattr(
                    user_data,
                    "profile_image",
                    None,
                ),
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
            
    def register(
        self,
        user_data,
    ) -> dict[str, Any]:
        """
        Register a new user.
        """