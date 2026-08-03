def test_stock_movements(
    client,
    auth_headers,
    test_product,
):
    # Create IN transaction
    response = client.post(
        "/inventory/transactions",
        headers=auth_headers,
        json={
            "product_id": test_product["id"],
            "transaction_type": "IN",
            "quantity": 50,
            "note": "Stock entry",
        },
    )

    assert response.status_code == 201

    # Get stock movements
    response = client.get(
        "/inventory/stock-movements",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1

    movement = next(
        item for item in data
        if item["product_id"] == test_product["id"]
    )

    assert movement["product_name"] == test_product["name"]
    assert movement["total_in"] == 50
    assert movement["total_out"] == 0