def test_product_history(
    client,
    auth_headers,
    test_product,
):
    # Create inventory transaction
    create_response = client.post(
        "/inventory/transactions",
        headers=auth_headers,
        json={
            "product_id": test_product["id"],
            "transaction_type": "IN",
            "quantity": 20,
            "note": "Initial stock",
        },
    )

    assert create_response.status_code == 201

    # Get product history
    response = client.get(
        f"/inventory/products/{test_product['id']}/history",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    transaction = data[0]

    assert transaction["product_id"] == test_product["id"]
    assert transaction["quantity"] == 20
    assert transaction["transaction_type"] == "IN"
    assert transaction["note"] == "Initial stock"