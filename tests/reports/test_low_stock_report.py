# =====================================================
# LOW STOCK REPORT EMPTY
# =====================================================


def test_low_stock_report_empty(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/low-stock",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data == []



# =====================================================
# LOW STOCK REPORT WITH PRODUCTS
# =====================================================


def test_low_stock_report_with_products(
    client,
    auth_headers,
    test_product,
):

    response = client.get(
        "/reports/low-stock?threshold=100",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["id"] == test_product["id"]

    assert data[0]["name"] == test_product["name"]

    assert data[0]["stock"] == test_product["stock"]



# =====================================================
# LOW STOCK REPORT SUCCESS
# =====================================================


def test_low_stock_report_success(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/low-stock",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)



# =====================================================
# LOW STOCK REPORT WITHOUT AUTHORIZATION
# =====================================================


def test_low_stock_report_without_token(
    client,
):

    response = client.get(
        "/reports/low-stock",
    )

    assert response.status_code == 401



# =====================================================
# LOW STOCK REPORT FORBIDDEN FOR NORMAL USER
# =====================================================


def test_low_stock_report_forbidden_for_user(
    client,
    user_token,
):

    response = client.get(
        "/reports/low-stock",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 403