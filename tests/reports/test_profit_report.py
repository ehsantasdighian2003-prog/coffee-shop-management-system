def test_profit_report_empty(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/profit",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    print("\nPROFIT RESPONSE:", data)

    assert data["total_revenue"] == "0"
    assert data["total_cost"] == "0"
    assert data["total_profit"] == "0"



def test_profit_report_with_orders(
    client,
    auth_headers,
    create_order,
):

    create_order(
        100000
    )

    create_order(
        200000
    )


    response = client.get(
        "/reports/profit",
        headers=auth_headers,
    )


    assert response.status_code == 200


    data = response.json()


    assert data["total_revenue"] == "300000"

    assert data["total_cost"] == "0"

    assert data["total_profit"] == "300000"



# =====================================================
# PROFIT REPORT WITHOUT AUTHORIZATION
# =====================================================


def test_profit_report_without_token(
    client,
):

    response = client.get(
        "/reports/profit",
    )

    assert response.status_code == 401



# =====================================================
# PROFIT REPORT FORBIDDEN FOR NORMAL USER
# =====================================================


def test_profit_report_forbidden_for_user(
    client,
    user_token,
):

    response = client.get(
        "/reports/profit",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 403