def test_get_warehouse_inventory(
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

    category = category_response.json()

    category_id = category["id"]


    # =========================
    # CREATE PRODUCT
    # =========================

    product_response = client.post(
        "/products",
        headers=auth_headers,
        json={
            "name": "Arabica Coffee",
            "description": "Premium coffee beans",
            "price": 10,
            "stock": 100,
            "category_id": category_id,
        },
    )

    assert product_response.status_code == 201

    product = product_response.json()

    product_id = product["id"]


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

    warehouse = warehouse_response.json()

    warehouse_id = warehouse["id"]


    # =========================
    # ADD PRODUCT
    # =========================

    add_response = client.post(
        f"/warehouses/{warehouse_id}/products",
        headers=auth_headers,
        json={
            "product_id": product_id,
            "quantity": 20,
        },
    )

    assert add_response.status_code == 200


    # =========================
    # GET INVENTORY
    # =========================

    response = client.get(
        f"/warehouses/{warehouse_id}/inventory",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    inventory = data[0]

    assert inventory["warehouse_id"] == warehouse_id
    assert inventory["product_id"] == product_id
    assert inventory["product_name"] == "Arabica Coffee"
    assert inventory["quantity"] == 20