def test_low_stock_report_empty(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/low-stock",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []



def test_low_stock_report_with_products(
    client,
    auth_headers,
    test_category,
):

    client.post(
        "/products/",
        headers=auth_headers,
        json={
            "name": "Espresso",
            "description": "Coffee",
            "price": 5,
            "stock": 3,
            "is_active": True,
            "category_id": test_category["id"],
        },
    )

    client.post(
        "/products/",
        headers=auth_headers,
        json={
            "name": "Latte",
            "description": "Coffee",
            "price": 6,
            "stock": 40,
            "is_active": True,
            "category_id": test_category["id"],
        },
    )


    response = client.get(
        "/reports/low-stock",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["name"] == "Espresso"
    assert data[0]["stock"] == 3