import pytest

from app.core.database import get_connection


@pytest.fixture
def create_report_order():

    def _create_report_order(
        product_id: int,
        quantity: int,
        price
    ):

        conn = get_connection()

        cursor = conn.cursor()

        # Create order

        cursor.execute(
    """
    INSERT INTO orders
    (
        user_id,
        total_price,
        payment_method
    )

    VALUES
    (
        %s,
        %s,
        %s
    )

    RETURNING id;
    """,
    (
        1,
        quantity * price,
        "cash"
    ),
)

        order_id = cursor.fetchone()[0]


        # Create order item

        cursor.execute(
            """
            INSERT INTO order_items
            (
                order_id,
                product_id,
                quantity,
                price
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s
            );
            """,
            (
                order_id,
                product_id,
                quantity,
                price
            ),
        )


        conn.commit()

        cursor.close()
        conn.close()


        return order_id


    return _create_report_order