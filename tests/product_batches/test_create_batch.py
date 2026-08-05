from datetime import date


def test_create_product_batch(
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
    # CREATE BATCH
    # =========================

    response = client.post(
        "/product-batches",
        headers=auth_headers,
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "batch_number": "ARB-001",
            "quantity": 50,
            "production_date": "2026-08-01",
            "expiration_date": "2026-09-01",
        },
    )


    assert response.status_code == 201

    data = response.json()


    assert data["product_id"] == product_id
    assert data["warehouse_id"] == warehouse_id
    assert data["batch_number"] == "ARB-001"
    assert data["quantity"] == 50