from datetime import date, timedelta


def test_get_expiring_batches(
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
    # CREATE EXPIRING BATCH
    # =========================

    expiration_date = (
        date.today() + timedelta(days=10)
    )

    batch_response = client.post(
        "/product-batches",
        headers=auth_headers,
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "batch_number": "ARB-EXP-001",
            "quantity": 30,
            "production_date": str(date.today()),
            "expiration_date": str(expiration_date),
        },
    )

    assert batch_response.status_code == 201


    # =========================
    # GET EXPIRING BATCHES
    # =========================

    response = client.get(
        "/product-batches/expiring",
        headers=auth_headers,
        params={
            "days": 30,
        },
    )


    assert response.status_code == 200

    data = response.json()


    assert len(data) >= 1

    batch = data[0]


    assert batch["product_id"] == product_id
    assert batch["warehouse_id"] == warehouse_id
    assert batch["batch_number"] == "ARB-EXP-001"
    assert batch["quantity"] == 30