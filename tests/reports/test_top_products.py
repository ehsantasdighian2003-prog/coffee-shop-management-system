def test_top_products_empty(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/top-products",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data == []



def test_top_products_with_orders(
    client,
    auth_headers,
    test_product,
    create_report_order,
):

    product = test_product


    create_report_order(
        product_id=product["id"],
        quantity=10,
        price=50000,
    )


    response = client.get(
        "/reports/top-products",
        headers=auth_headers,
    )


    assert response.status_code == 200


    data = response.json()


    assert len(data) == 1


    assert data[0]["product_name"] == "Espresso"

    assert data[0]["total_sold"] == 10

    assert data[0]["revenue"] == "500000"
    
    
# =====================================================
# TOP PRODUCTS REPORT SUCCESS
# =====================================================

def test_top_products_report_success(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/top-products",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    
    
# =====================================================
# TOP PRODUCTS REPORT WITHOUT AUTHORIZATION
# =====================================================

def test_top_products_without_token(client):

    response = client.get("/reports/top-products")

    assert response.status_code == 401


# =====================================================
# TOP PRODUCTS REPORT FORBIDDEN FOR NORMAL USER
# =====================================================

def test_top_products_forbidden_for_user(
    client,
    user_token,
):

    response = client.get(
        "/reports/top-products",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 403