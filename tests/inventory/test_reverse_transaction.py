def test_reverse_inventory_transaction(
    client,
    auth_headers,
    test_product,
):
    # Create initial IN transaction
    create_response = client.post(
        "/inventory/transactions",
        headers=auth_headers,
        json={
            "product_id": test_product["id"],
            "transaction_type": "IN",
            "quantity": 30,
            "note": "Initial stock",
        },
    )

    assert create_response.status_code == 201

    transaction = create_response.json()

    transaction_id = transaction["id"]

    # Reverse transaction
    reverse_response = client.post(
        f"/inventory/transactions/{transaction_id}/reverse",
        headers=auth_headers,
        json={
            "note": "Correction",
        },
    )

    assert reverse_response.status_code == 200

    reversed_transaction = reverse_response.json()

    assert reversed_transaction["product_id"] == test_product["id"]
    assert reversed_transaction["transaction_type"] == "OUT"
    assert reversed_transaction["quantity"] == 30
    assert reversed_transaction["note"] == "Correction"