def test_create_product(client, auth_headers, test_category):

    response = client.post(
        "/products/",
        headers=auth_headers,
        json={
            "name": "Latte",
            "description": "Milk coffee",
            "price": 6,
            "stock": 20,
            "is_active": True,
            "category_id": test_category["id"],
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Latte"
    assert data["price"] == 6
    assert data["stock"] == 20
    assert data["category_id"] == test_category["id"]
