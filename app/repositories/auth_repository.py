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
                    role,
                    is_active
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
                    role,
                    is_active
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
        password: str,
        first_name=None,
        last_name=None,
        email=None,
        phone_number=None,
        profile_image=None,
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

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
                )
            )

            return cur.fetchone()

    # =========================
    # UPDATE LAST LOGIN
    # =========================

    @staticmethod
    def update_last_login(
        conn,
        user_id: int
    ):

        with conn.cursor() as cur:

            cur.execute(
                """
                UPDATE users
                SET last_login = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (user_id,)
            )