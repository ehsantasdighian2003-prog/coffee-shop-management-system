from typing import Any

from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor


class AuthRepository:
    """
    Repository responsible for all authentication-related
    database operations.
    """

    def __init__(self, conn: connection):
        self.conn = conn

    # ==================================================
    # PRIVATE HELPERS
    # ==================================================

    def _cursor(self):
        return self.conn.cursor(cursor_factory=RealDictCursor)

    # ==================================================
    # GET USER BY USERNAME
    # ==================================================

    def get_user_by_username(
        self,
        username: str,
    ) -> dict[str, Any] | None:

        with self._cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    username,
                    password,
                    role,
                    is_active
                FROM users
                WHERE username = %s
                """,
                (username,),
            )

            return cur.fetchone()

    # ==================================================
    # GET USER BY EMAIL
    # ==================================================

    def get_user_by_email(
        self,
        email: str,
    ) -> dict[str, Any] | None:

        with self._cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    username,
                    email,
                    role,
                    is_active
                FROM users
                WHERE email = %s
                """,
                (email,),
            )

            return cur.fetchone()

    # ==================================================
    # GET USER BY ID
    # ==================================================

    def get_user_by_id(
        self,
        user_id: int,
    ) -> dict[str, Any] | None:

        with self._cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    username,
                    role,
                    is_active
                FROM users
                WHERE id = %s
                """,
                (user_id,),
            )

            return cur.fetchone()

    # ==================================================
    # CREATE USER
    # ==================================================

    def create_user(
        self,
        username: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone_number: str | None = None,
        profile_image: str | None = None,
    ) -> dict[str, Any] | None:

        with self._cursor() as cur:

            cur.execute(
                """
                INSERT INTO users (
                    username,
                    password,
                    first_name,
                    last_name,
                    email,
                    phone_number,
                    profile_image
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING
                    id,
                    username,
                    role
                """,
                (
                    username,
                    password,
                    first_name,
                    last_name,
                    email,
                    phone_number,
                    profile_image,
                ),
            )

            return cur.fetchone()

    # ==================================================
    # UPDATE LAST LOGIN
    # ==================================================

    def update_last_login(
        self,
        user_id: int,
    ) -> None:

        with self.conn.cursor() as cur:

            cur.execute(
                """
                UPDATE users
                SET last_login = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (user_id,),
            )

    # ==================================================
    # DEACTIVATE USER
    # ==================================================

    def deactivate_user(
        self,
        user_id: int,
    ) -> None:

        with self.conn.cursor() as cur:

            cur.execute(
                """
                UPDATE users
                SET is_active = FALSE
                WHERE id = %s
                """,
                (user_id,),
            )