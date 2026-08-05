def test_receive_purchase_order_creates_inventory_transaction(
    client,
    auth_headers,
    test_product,
    test_supplier,
):

    # =========================
    # CREATE PURCHASE ORDER
    # =========================

    response = client.post(
        "/purchase-orders",
        headers=auth_headers,
        json={
            "supplier_id": test_supplier["id"],
            "notes": "Inventory transaction test",
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": 30,
                    "unit_price": 5,
                }
            ],
        },
    )

    assert response.status_code == 200

    purchase_order = response.json()

    purchase_order_id = purchase_order["id"]


    # =========================
    # RECEIVE PURCHASE ORDER
    # =========================

    response = client.put(
        f"/purchase-orders/{purchase_order_id}/receive",
        headers=auth_headers,
    )

    assert response.status_code == 200


    # =========================
    # CHECK INVENTORY HISTORY
    # =========================

    response = client.get(
        f"/inventory/products/{test_product['id']}/history",
        headers=auth_headers,
    )

    assert response.status_code == 200

    transactions = response.json()


    transaction = next(
        item
        for item in transactions
        if item["note"] == "purchase_order_received"
    )


    assert transaction["product_id"] == test_product["id"]

    assert transaction["transaction_type"] == "IN"

    assert transaction["quantity"] == 30