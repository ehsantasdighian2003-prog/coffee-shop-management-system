def test_inventory_updates_low_stock_report(
    client,
    auth_headers,
    test_product,
):
    response = client.post(
        "/inventory/transactions",
        headers=auth_headers,
        json={
            "product_id": test_product["id"],
            "transaction_type": "OUT",
            "quantity": 95,
            "note": "Low stock test",
        },
    )

    assert response.status_code == 201

    response = client.get(
        "/reports/low-stock",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    product_ids = [
        item["id"]
        for item in data
    ]

    assert test_product["id"] in product_ids