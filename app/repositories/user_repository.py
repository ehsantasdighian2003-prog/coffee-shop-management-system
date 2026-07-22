from typing import Any

from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor


class UserRepository:
    """
    Repository responsible for user database operations.
    """


    def __init__(
        self,
        conn: connection
    ):
        self.conn = conn



    # ==================================================
    # PRIVATE HELPERS
    # ==================================================


    def _cursor(self):

        return self.conn.cursor(
            cursor_factory=RealDictCursor
        )



    # ==================================================
    # CREATE USER
    # ==================================================


    def create_user(
        self,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        email: str,
        role: str = "user",
    ) -> dict[str, Any] | None:


        with self._cursor() as cur:

            cur.execute(
                """
                INSERT INTO users
                (
                    username,
                    password,
                    first_name,
                    last_name,
                    email,
                    role
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )

                RETURNING *
                """,
                (
                    username,
                    password,
                    first_name,
                    last_name,
                    email,
                    role,
                ),
            )


            return cur.fetchone()



    # ==================================================
    # GET USER BY ID
    # ==================================================


    def get_by_id(
        self,
        user_id: int,
    ) -> dict[str, Any] | None:


        with self._cursor() as cur:

            cur.execute(
                """
                SELECT *
                FROM users

                WHERE id = %s
                AND deleted_at IS NULL
                """,
                (
                    user_id,
                ),
            )


            return cur.fetchone()



    # ==================================================
    # GET USER BY USERNAME
    # ==================================================


    def get_by_username(
        self,
        username: str,
    ) -> dict[str, Any] | None:


        with self._cursor() as cur:

            cur.execute(
                """
                SELECT *
                FROM users

                WHERE username = %s
                AND deleted_at IS NULL
                """,
                (
                    username,
                ),
            )


            return cur.fetchone()



    # ==================================================
    # GET USER BY EMAIL
    # ==================================================


    def get_by_email(
        self,
        email: str,
    ) -> dict[str, Any] | None:


        with self._cursor() as cur:

            cur.execute(
                """
                SELECT *
                FROM users

                WHERE email = %s
                AND deleted_at IS NULL
                """,
                (
                    email,
                ),
            )


            return cur.fetchone()



    # ==================================================
    # GET ALL USERS
    # ==================================================


    def get_all(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict[str, Any]]:


        with self._cursor() as cur:

            cur.execute(
                """
                SELECT *
                FROM users

                WHERE deleted_at IS NULL

                ORDER BY id DESC

                LIMIT %s
                OFFSET %s
                """,
                (
                    limit,
                    offset,
                ),
            )


            return cur.fetchall()



    # ==================================================
    # COUNT USERS
    # ==================================================


    def count_users(
        self,
    ) -> int:


        with self.conn.cursor() as cur:

            cur.execute(
                """
                SELECT COUNT(*)

                FROM users

                WHERE deleted_at IS NULL
                """
            )


            return cur.fetchone()[0]



    # ==================================================
    # UPDATE PROFILE
    # ==================================================


    def update_user(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str | None = None,
        profile_image: str | None = None,
    ) -> dict[str, Any] | None:


        with self._cursor() as cur:

            cur.execute(
                """
                UPDATE users

                SET
                    first_name = %s,
                    last_name = %s,
                    email = %s,
                    phone_number = %s,
                    profile_image = %s,
                    updated_at = NOW()

                WHERE id = %s
                AND deleted_at IS NULL

                RETURNING *
                """,
                (
                    first_name,
                    last_name,
                    email,
                    phone_number,
                    profile_image,
                    user_id,
                ),
            )


            return cur.fetchone()



    # ==================================================
    # UPDATE PASSWORD
    # ==================================================


    def update_password(
        self,
        user_id: int,
        password: str,
    ) -> dict[str, Any] | None:


        with self._cursor() as cur:

            cur.execute(
                """
                UPDATE users

                SET
                    password = %s,
                    updated_at = NOW()

                WHERE id = %s
                AND deleted_at IS NULL

                RETURNING *
                """,
                (
                    password,
                    user_id,
                ),
            )


            return cur.fetchone()



    # ==================================================
    # UPDATE ROLE
    # ==================================================


    def update_role(
        self,
        user_id: int,
        role: str,
    ) -> dict[str, Any] | None:


        with self._cursor() as cur:

            cur.execute(
                """
                UPDATE users

                SET
                    role = %s,
                    updated_at = NOW()

                WHERE id = %s
                AND deleted_at IS NULL

                RETURNING *
                """,
                (
                    role,
                    user_id,
                ),
            )


            return cur.fetchone()



    # ==================================================
    # ACTIVATE USER
    # ==================================================


    def activate_user(
        self,
        user_id: int,
    ) -> dict[str, Any] | None:


        with self._cursor() as cur:

            cur.execute(
                """
                UPDATE users

                SET
                    is_active = TRUE,
                    updated_at = NOW()

                WHERE id = %s
                AND deleted_at IS NULL

                RETURNING *
                """,
                (
                    user_id,
                ),
            )


            return cur.fetchone()



    # ==================================================
    # DEACTIVATE USER
    # ==================================================


    def deactivate_user(
        self,
        user_id: int,
    ) -> dict[str, Any] | None:


        with self._cursor() as cur:

            cur.execute(
                """
                UPDATE users

                SET
                    is_active = FALSE,
                    updated_at = NOW()

                WHERE id = %s
                AND deleted_at IS NULL

                RETURNING *
                """,
                (
                    user_id,
                ),
            )


            return cur.fetchone()



    # ==================================================
    # SOFT DELETE
    # ==================================================


    def soft_delete_user(
        self,
        user_id: int,
    ) -> dict[str, Any] | None:


        with self._cursor() as cur:

            cur.execute(
                """
                UPDATE users

                SET
                    deleted_at = NOW(),
                    is_active = FALSE,
                    updated_at = NOW()

                WHERE id = %s
                AND deleted_at IS NULL

                RETURNING *
                """,
                (
                    user_id,
                ),
            )


            return cur.fetchone()



    # ==================================================
    # RESTORE USER
    # ==================================================


    def restore_user(
        self,
        user_id: int,
    ) -> dict[str, Any] | None:


        with self._cursor() as cur:

            cur.execute(
                """
                UPDATE users

                SET
                    deleted_at = NULL,
                    is_active = TRUE,
                    updated_at = NOW()

                WHERE id = %s

                RETURNING *
                """,
                (
                    user_id,
                ),
            )


            return cur.fetchone()