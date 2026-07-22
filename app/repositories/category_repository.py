from psycopg2.extras import RealDictCursor


class CategoryRepository:

    def __init__(self, conn):
        self.conn = conn


    # =========================
    # BASE SELECT
    # =========================

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

    def create_category(
        self,
        name: str,
        description: str | None
    ):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

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

    def get_all_categories(self):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                self.CATEGORY_SELECT +
                """
                ORDER BY id ASC
                """
            )

            return cur.fetchall()



    # =========================
    # GET CATEGORY BY ID
    # =========================

    def get_category_by_id(
        self,
        category_id: int
    ):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                self.CATEGORY_SELECT +
                """
                WHERE id = %s
                """,
                (category_id,)
            )

            return cur.fetchone()



    # =========================
    # UPDATE CATEGORY
    # =========================

    def update_category(
        self,
        category_id: int,
        name: str,
        description: str | None
    ):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

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

    def delete_category(
        self,
        category_id: int
    ):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                DELETE FROM categories

                WHERE id = %s

                RETURNING id
                """,
                (category_id,)
            )

            return cur.fetchone()