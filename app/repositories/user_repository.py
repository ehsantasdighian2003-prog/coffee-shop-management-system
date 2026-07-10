from psycopg2.extras import RealDictCursor


class UserRepository:

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