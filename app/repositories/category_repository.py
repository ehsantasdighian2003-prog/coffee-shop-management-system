from psycopg2.extras import RealDictCursor


class CategoryRepository:


    CATEGORY_SELECT = """
        SELECT
            id,
            name,
            description,
            created_at

        FROM categories
    """


    # =========================
    # CREATE CATEGORY
    # =========================

    @staticmethod
    def create_category(
        conn,
        name: str,
        description: str | None
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                INSERT INTO categories
                (
                    name,
                    description
                )

                VALUES (%s, %s)

                RETURNING
                    id,
                    name,
                    description,
                    created_at
                """,
                (
                    name,
                    description
                )
            )

            return cur.fetchone()



    # =========================
    # GET ALL CATEGORIES
    # =========================

    @staticmethod
    def get_all_categories(
        conn
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                CategoryRepository.CATEGORY_SELECT +
                """
                ORDER BY id ASC
                """
            )

            return cur.fetchall()



    # =========================
    # GET CATEGORY BY ID
    # =========================

    @staticmethod
    def get_category_by_id(
        conn,
        category_id: int
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                CategoryRepository.CATEGORY_SELECT +
                """
                WHERE id = %s
                """,
                (category_id,)
            )

            return cur.fetchone()



    # =========================
    # UPDATE CATEGORY
    # =========================

    @staticmethod
    def update_category(
        conn,
        category_id: int,
        name: str,
        description: str | None
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                UPDATE categories

                SET
                    name = %s,
                    description = %s

                WHERE id = %s

                RETURNING
                    id,
                    name,
                    description,
                    created_at
                """,
                (
                    name,
                    description,
                    category_id
                )
            )

            return cur.fetchone()



    # =========================
    # DELETE CATEGORY
    # =========================

    @staticmethod
    def delete_category(
        conn,
        category_id: int
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                DELETE FROM categories

                WHERE id = %s

                RETURNING id
                """,
                (category_id,)
            )

            return cur.fetchone()
