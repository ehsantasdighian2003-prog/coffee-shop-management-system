# =====================================================
# BEST SELLING HOURS REPORT SUCCESS
# =====================================================


def test_best_selling_hours_report(client, auth_headers):

    response = client.get(
        "/reports/best-selling-hours",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if len(data) > 0:

        item = data[0]

        assert "hour" in item

        assert "total_orders" in item

        assert "revenue" in item
        
        
# =====================================================
# BEST SELLING HOURS WITHOUT AUTHORIZATION
# =====================================================


def test_best_selling_hours_without_token(client):

    response = client.get(
        "/reports/best-selling-hours",
    )

    assert response.status_code == 401
    
    
# =====================================================
# BEST SELLING HOURS FORBIDDEN FOR NORMAL USER
# =====================================================


def test_best_selling_hours_forbidden_for_user(
    client,
    user_token,
):

    response = client.get(
        "/reports/best-selling-hours",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 403
    
    
# =====================================================
# BEST SELLING HOURS REPORT WITH DATA
# =====================================================


def test_best_selling_hours_with_orders(
    client,
    auth_headers,
    test_product,
    user_token,
):

    order_response = client.post(
        "/orders/",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": 2,
                }
            ]
        },
    )

    assert order_response.status_code == 201


    response = client.get(
        "/reports/best-selling-hours",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    item = data[0]

    assert item["total_orders"] >= 1

    assert "revenue" in item