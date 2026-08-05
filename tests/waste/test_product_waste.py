def test_get_product_waste_history(
    client,
    auth_headers,
):

    # =========================
    # CREATE CATEGORY
    # =========================

    category_response = client.post(
        "/categories",
        headers=auth_headers,
        json={
            "name": "Coffee",
            "description": "Coffee products",
        },
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]


    # =========================
    # CREATE PRODUCT
    # =========================

    product_response = client.post(
        "/products",
        headers=auth_headers,
        json={
            "name": "Arabica Coffee",
            "description": "Premium beans",
            "price": 10,
            "stock": 100,
            "category_id": category_id,
        },
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]


    # =========================
    # CREATE WAREHOUSE
    # =========================

    warehouse_response = client.post(
        "/warehouses",
        headers=auth_headers,
        json={
            "name": "Main Warehouse",
            "location": "Tehran",
        },
    )

    assert warehouse_response.status_code == 201

    warehouse_id = warehouse_response.json()["id"]


    # =========================
    # CREATE WASTE
    # =========================

    waste_response = client.post(
        "/waste",
        headers=auth_headers,
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "quantity": 5,
            "reason": "Expired beans",
            "cost": 50,
        },
    )

    assert waste_response.status_code == 201


    # =========================
    # GET PRODUCT WASTE
    # =========================

    response = client.get(
        f"/waste/product/{product_id}",
        headers=auth_headers,
    )


    assert response.status_code == 200


    data = response.json()


    assert len(data) == 1

    assert data[0]["product_id"] == product_id

    assert data[0]["quantity"] == 5

    assert data[0]["reason"] == "Expired beans"