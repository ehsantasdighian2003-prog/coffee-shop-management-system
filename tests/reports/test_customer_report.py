def test_customer_report_empty(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/customers",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data == []



def test_customer_report_with_orders(
    client,
    auth_headers,
    test_category,
    test_product,
):
    # دریافت شناسه کاربر تست
    login = client.post(
        "/auth/login",
        json={
            "username": "admin_test",
            "password": "12345678",
        },
    )

    assert login.status_code == 200


    # ایجاد سفارش
    response = client.post(
        "/orders/",
        headers=auth_headers,
        json={
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": 2,
                }
            ]
        },
    )

    assert response.status_code == 201


    # دریافت گزارش
    response = client.get(
        "/reports/customers",
        headers=auth_headers,
    )

    assert response.status_code == 200


    data = response.json()


    assert len(data) == 1

    assert data[0]["username"] == "admin_test"

    assert data[0]["total_orders"] == 1

    assert data[0]["total_spent"] == "11"

    assert data[0]["average_order_value"] == "11"
    
    
# =====================================================
# CUSTOMER REPORT SUCCESS
# =====================================================


def test_customer_report_success(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/customers",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    
    
# =====================================================
# CUSTOMER REPORT WITHOUT AUTHORIZATION
# =====================================================


def test_customer_report_without_token(
    client,
):

    response = client.get(
        "/reports/customers",
    )

    assert response.status_code == 401



# =====================================================
# CUSTOMER REPORT FORBIDDEN FOR NORMAL USER
# =====================================================


def test_customer_report_forbidden_for_user(
    client,
    user_token,
):

    response = client.get(
        "/reports/customers",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 403