from typing import Any
from uuid import UUID

from psycopg2.extras import RealDictCursor


class CustomerRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_customer(self, customer_data: dict[str, Any]):
        query = """
            INSERT INTO customers (
                id,
                full_name,
                phone,
                email,
                birthday,
                address,
                gender
            )
            VALUES (
                gen_random_uuid(),
                %(full_name)s,
                %(phone)s,
                %(email)s,
                %(birthday)s,
                %(address)s,
                %(gender)s
            )
            RETURNING *
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(query, customer_data)
            return cursor.fetchone()

    def get_customer_by_id(
        self,
        customer_id: UUID,
    ):
        query = """
            SELECT *
            FROM customers
            WHERE id = %s
            AND is_deleted = FALSE
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(
                query,
                (str(customer_id),),
            )
            return cursor.fetchone()

    def get_customer_by_phone(
        self,
        phone: str,
    ):
        query = """
            SELECT *
            FROM customers
            WHERE phone = %s
            AND is_deleted = FALSE
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(
                query,
                (phone,),
            )
            return cursor.fetchone()

    def get_customers(
        self,
        limit: int = 20,
        offset: int = 0,
    ):
        query = """
            SELECT *
            FROM customers
            WHERE is_deleted = FALSE
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(
                query,
                (limit, offset),
            )
            return cursor.fetchall()

    def update_customer(
        self,
        customer_id: UUID,
        customer_data: dict,
    ):

        update_data = {
            "id": str(customer_id),
            "full_name": customer_data.get("full_name"),
            "phone": customer_data.get("phone"),
            "email": customer_data.get("email"),
            "birthday": customer_data.get("birthday"),
            "address": customer_data.get("address"),
            "gender": customer_data.get("gender"),
        }

        query = """
            UPDATE customers
            SET
                full_name = COALESCE(%(full_name)s, full_name),
                phone = COALESCE(%(phone)s, phone),
                email = COALESCE(%(email)s, email),
                birthday = COALESCE(%(birthday)s, birthday),
                address = COALESCE(%(address)s, address),
                gender = COALESCE(%(gender)s, gender),
                updated_at = NOW()
            WHERE id = %(id)s
            AND is_deleted = FALSE
            RETURNING *
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(
                query,
                update_data,
            )

            return cursor.fetchone()

    def soft_delete_customer(
        self,
        customer_id: UUID,
    ):
        query = """
            UPDATE customers
            SET
                is_deleted = TRUE,
                is_active = FALSE,
                updated_at = NOW()
            WHERE id = %s
            RETURNING *
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(
                query,
                (str(customer_id),),
            )

            return cursor.fetchone()

    def restore_customer(
        self,
        customer_id: UUID,
    ):
        query = """
            UPDATE customers
            SET
                is_deleted = FALSE,
                is_active = TRUE,
                updated_at = NOW()
            WHERE id = %s
            RETURNING *
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(
                query,
                (str(customer_id),),
            )

            return cursor.fetchone()