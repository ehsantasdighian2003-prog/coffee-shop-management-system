# =====================================================
# CREATE ORDER SUCCESS
# =====================================================


def test_create_order_success(client, user_token, test_product):

    response = client.post(
        "/orders/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "payment_method": "cash",
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": 2,
                }
            ],
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "order_id" in data
    assert data["user_id"] is not None

    assert data["payment_method"] == "cash"

    assert len(data["items"]) == 1

    assert data["items"][0]["product_id"] == test_product["id"]

    assert data["items"][0]["quantity"] == 2

    assert float(data["total_price"]) == 11.0


# =====================================================
# STOCK DECREASE AFTER ORDER
# =====================================================


def test_order_decreases_product_stock(client, user_token, test_product):

    initial_stock = test_product["stock"]

    response = client.post(
        "/orders/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "payment_method": "cash",
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": 5,
                }
            ],
        },
    )

    assert response.status_code == 201

    # Get product after order

    product_response = client.get(f"/products/{test_product['id']}")

    assert product_response.status_code == 200

    product = product_response.json()

    assert product["stock"] == initial_stock - 5


# =====================================================
# CREATE ORDER WITH INVALID PRODUCT
# =====================================================


def test_create_order_with_invalid_product(client, user_token):

    response = client.post(
        "/orders/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "payment_method": "cash",
            "items": [
                {
                    "product_id": 999999,
                    "quantity": 1,
                }
            ],
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["success"] is False

    assert data["message"] == "Product 999999 not found."


# =====================================================
# CREATE ORDER WITH INSUFFICIENT STOCK
# =====================================================


def test_create_order_with_insufficient_stock(client, user_token, test_product):

    response = client.post(
        "/orders/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "payment_method": "cash",
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": test_product["stock"] + 1,
                }
            ],
        },
    )

    assert response.status_code == 409

    data = response.json()

    assert data["success"] is False

    assert (
        f"Not enough stock for product {test_product['id']}."
        in data["message"]
    )