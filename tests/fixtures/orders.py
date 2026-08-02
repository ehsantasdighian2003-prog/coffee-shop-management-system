import pytest

from app.core.database import get_connection


@pytest.fixture
def create_order():

    def _create_order(
        total_price,
        quantity=1,
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO orders
(
    customer_name,
    quantity,
    total_price,
    status,
    payment_method
)
VALUES
(
    %s,
    %s,
    %s,
    %s,
    %s
)
RETURNING id;
            """,
            (
    "Test Customer",
    quantity,
    total_price,
    "completed",
    "cash",
),
        )

        order_id = cursor.fetchone()[0]

        conn.commit()

        cursor.close()
        conn.close()

        return order_id

    return _create_order