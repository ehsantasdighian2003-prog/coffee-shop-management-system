def test_dashboard_report_empty(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/dashboard",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["users"] == 1
    assert data["products"] == 0
    assert data["categories"] == 0
    assert data["orders"] == 0

    assert data["total_revenue"] == "0"
    assert data["average_order_value"] == "0"



def test_dashboard_report_with_orders(
    client,
    auth_headers,
    create_order,
):

    create_order(100000)

    create_order(200000)


    response = client.get(
        "/reports/dashboard",
        headers=auth_headers,
    )


    assert response.status_code == 200


    data = response.json()


    assert data["orders"] == 2

    assert data["total_revenue"] == "300000"

    assert data["average_order_value"] == "150000"
    
    
# =====================================================
# DASHBOARD REPORT SUCCESS
# =====================================================


def test_dashboard_report_success(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/dashboard",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "users" in data

    assert "products" in data

    assert "categories" in data

    assert "orders" in data

    assert "total_revenue" in data

    assert "average_order_value" in data
    
    
# =====================================================
# DASHBOARD REPORT WITHOUT AUTHORIZATION
# =====================================================

def test_dashboard_report_without_token(
    client,
):

    response = client.get(
        "/reports/dashboard",
    )

    assert response.status_code == 401