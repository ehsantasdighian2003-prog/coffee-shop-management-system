def test_create_inventory_transaction(
    client,
    auth_headers,
    test_product,
):

    response = client.post(
        "/inventory/transactions",
        headers=auth_headers,
        json={
            "product_id": test_product["id"],
            "transaction_type": "IN",
            "quantity": 20,
            "note": "Initial stock",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["product_id"] == test_product["id"]
    assert data["quantity"] == 20
    assert data["transaction_type"] == "IN"