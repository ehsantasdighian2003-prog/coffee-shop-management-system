def test_daily_sales_empty(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/daily-sales",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []



def test_daily_sales_with_orders(
    client,
    auth_headers,
    test_category,
):

    # Create product
    product_response = client.post(
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
    )

    assert product_response.status_code == 201

    product = product_response.json()


    # Create customer
    register_response = client.post(
        "/auth/register",
        json={
            "username": "daily_user",
            "email": "daily@test.com",
            "password": "12345678",
        },
    )

    assert register_response.status_code == 201


    # Login customer
    login_response = client.post(
        "/auth/login",
        json={
            "username": "daily_user",
            "password": "12345678",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]


    order_response = client.post(
        "/orders/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2,
                }
            ]
        },
    )

    assert order_response.status_code == 201


    # Get daily sales report
    report_response = client.get(
        "/reports/daily-sales",
        headers=auth_headers,
    )

    assert report_response.status_code == 200


    data = report_response.json()

    assert len(data) == 1

    assert data[0]["total_orders"] == 1

    assert float(
        data[0]["revenue"]
    ) == 10.0

    assert float(
        data[0]["average_order_value"]
    ) == 10.0
    
    
def test_daily_sales_without_token(
    client,
):

    response = client.get(
        "/reports/daily-sales",
    )

    assert response.status_code == 401



def test_daily_sales_forbidden_for_user(
    client,
    user_token,
):

    response = client.get(
        "/reports/daily-sales",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 403