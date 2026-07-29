def test_category_performance_empty(client):

    response = client.get("/reports/category-performance")

    assert response.status_code == 200
    assert response.json() == []


def test_category_performance_with_orders(
    client,
    auth_headers,
    test_category,
):
    # Create product
    product = client.post(
        "/products/",
        headers=auth_headers,
        json={
            "name": "Espresso",
            "description": "Coffee",
            "price": 5,
            "stock": 100,
            "is_active": True,
            "category_id": test_category["id"],
        },
    ).json()

    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "customer",
            "email": "customer@test.com",
            "password": "12345678",
        },
    )

    login = client.post(
        "/auth/login",
        json={
            "username": "customer",
            "password": "12345678",
        },
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create order
    client.post(
        "/orders/",
        headers=headers,
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2,
                }
            ]
        },
    )

    response = client.get("/reports/category-performance")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["category_name"] == "Coffee"
    assert data[0]["total_sold"] == 2
    assert float(data[0]["revenue"]) == 10.0