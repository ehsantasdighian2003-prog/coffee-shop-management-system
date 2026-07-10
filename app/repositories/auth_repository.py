from psycopg2.extras import RealDictCursor


class AuthRepository:

    # =========================
    # GET USER BY USERNAME
    # =========================
    @staticmethod
    def get_user_by_username(
        conn,
        username: str
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                SELECT
                    id,
                    username,
                    password,
                    role
                FROM users
                WHERE username = %s
                """,
                (username,)
            )

            return cur.fetchone()

    # =========================
    # GET USER BY ID
    # =========================
    @staticmethod
    def get_user_by_id(
        conn,
        user_id: int
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                SELECT
                    id,
                    username,
                    role
                FROM users
                WHERE id = %s
                """,
                (user_id,)
            )

            return cur.fetchone()

    # =========================
    # CREATE USER
    # =========================
    @staticmethod
    def create_user(
        conn,
        username: str,
        hashed_password: str
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                INSERT INTO users (
                    username,
                    password
                )
                VALUES (%s, %s)
                RETURNING
                    id,
                    username,
                    role
                """,
                (
                    username,
                    hashed_password
                )
            )

            return cur.fetchone()