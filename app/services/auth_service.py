from app.core.database import get_connection
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

        conn = get_connection()

        try:

            existing_user = self.repo.get_user_by_username(
                conn,
                user_data.username
            )

            if existing_user:
                raise UsernameAlreadyExistsException()

            hashed_password = pwd_context.hash(
                user_data.password
            )

            user = self.repo.create_user(
                conn,
                user_data.username,
                hashed_password
            )

            conn.commit()

            return {
                "message": "User registered successfully.",
                "user_id": user["id"]
            }

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    # =========================
    # LOGIN
    # =========================
    def login(self, user_data):

        conn = get_connection()

        try:

            user = self.repo.get_user_by_username(
                conn,
                user_data.username
            )

            if not user:
                raise AuthenticationException(
                    "Invalid username or password"
                )

            if not verify_password(
                user_data.password,
                user["password"]
            ):
                raise AuthenticationException(
                    "Invalid username or password"
                )

            access_token = create_access_token(
                {
                    "user_id": user["id"]
                }
            )

            return {
                "access_token": access_token,
                "token_type": "bearer"
            }

        finally:
            conn.close()