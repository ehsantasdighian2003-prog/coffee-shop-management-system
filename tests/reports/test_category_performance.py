# =====================================================
# CATEGORY PERFORMANCE EMPTY
# =====================================================


def test_category_performance_empty(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/category-performance",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data == []



# =====================================================
# CATEGORY PERFORMANCE WITH ORDERS
# =====================================================


def test_category_performance_with_orders(
    client,
    auth_headers,
    create_report_order,
    test_product,
):

    create_report_order(
    product_id=test_product["id"],
    quantity=2,
    price=5.5,
)

    response = client.get(
        "/reports/category-performance",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    assert "category_name" in data[0]

    assert "total_sold" in data[0]

    assert "revenue" in data[0]



# =====================================================
# CATEGORY PERFORMANCE SUCCESS
# =====================================================


def test_category_performance_success(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/category-performance",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)



# =====================================================
# CATEGORY PERFORMANCE WITHOUT TOKEN
# =====================================================


def test_category_performance_without_token(
    client,
):

    response = client.get(
        "/reports/category-performance",
    )

    assert response.status_code == 401



# =====================================================
# CATEGORY PERFORMANCE FORBIDDEN FOR USER
# =====================================================


def test_category_performance_forbidden_for_user(
    client,
    user_token,
):

    response = client.get(
        "/reports/category-performance",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 403