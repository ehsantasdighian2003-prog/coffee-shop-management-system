from psycopg2.extras import RealDictCursor


class UserRepository:

    # =========================
    # CREATE USER
    # =========================

    def create_user(
        self,
        conn,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        email: str,
        role: str = "user"
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

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
                    role
                )
            )

            return cur.fetchone()


    # =========================
    # GET USER BY ID
    # =========================

    def get_by_id(
        self,
        conn,
        user_id: int
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT *
                FROM users
                WHERE id = %s
                AND deleted_at IS NULL
                """,
                (user_id,)
            )

            return cur.fetchone()


    # =========================
    # GET USER BY USERNAME
    # =========================

    def get_by_username(
        self,
        conn,
        username: str
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT *
                FROM users
                WHERE username = %s
                AND deleted_at IS NULL
                """,
                (username,)
            )

            return cur.fetchone()


    # =========================
    # GET USER BY EMAIL
    # =========================

    def get_by_email(
        self,
        conn,
        email: str
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT *
                FROM users
                WHERE email = %s
                AND deleted_at IS NULL
                """,
                (email,)
            )

            return cur.fetchone()


    # =========================
    # GET ALL USERS
    # =========================

    def get_all(
        self,
        conn,
        limit: int = 20,
        offset: int = 0
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

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
                    offset
                )
            )

            return cur.fetchall()


    # =========================
    # COUNT USERS
    # =========================

    def count_users(
        self,
        conn
    ):

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT COUNT(*)
                FROM users
                WHERE deleted_at IS NULL
                """
            )

            return cur.fetchone()[0]


    # =========================
    # UPDATE USER
    # =========================

    def update_user(
        self,
        conn,
        user_id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str = None,
        profile_image: str = None
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

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
                    user_id
                )
            )

            return cur.fetchone()


    # =========================
    # UPDATE PASSWORD
    # =========================

    def update_password(
        self,
        conn,
        user_id: int,
        password: str
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

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
                    user_id
                )
            )

            return cur.fetchone()


    # =========================
    # UPDATE ROLE
    # =========================

    def update_role(
        self,
        conn,
        user_id: int,
        role: str
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

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
                    user_id
                )
            )

            return cur.fetchone()


    # =========================
    # ACTIVATE USER
    # =========================

    def activate_user(
        self,
        conn,
        user_id: int
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                UPDATE users
                SET
                    is_active = TRUE,
                    updated_at = NOW()
                WHERE id = %s
                RETURNING *
                """,
                (user_id,)
            )

            return cur.fetchone()


    # =========================
    # DEACTIVATE USER
    # =========================

    def deactivate_user(
        self,
        conn,
        user_id: int
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                UPDATE users
                SET
                    is_active = FALSE,
                    updated_at = NOW()
                WHERE id = %s
                RETURNING *
                """,
                (user_id,)
            )

            return cur.fetchone()


    # =========================
    # SOFT DELETE USER
    # =========================

    def soft_delete_user(
        self,
        conn,
        user_id: int
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                UPDATE users
                SET
                    deleted_at = NOW(),
                    is_active = FALSE
                WHERE id = %s
                AND deleted_at IS NULL
                RETURNING *
                """,
                (user_id,)
            )

            return cur.fetchone()


    # =========================
    # RESTORE USER
    # =========================

    def restore_user(
        self,
        conn,
        user_id: int
    ):

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

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
                (user_id,)
            )

            return cur.fetchone()