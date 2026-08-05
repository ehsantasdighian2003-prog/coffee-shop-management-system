def test_create_purchase_order(
    client,
    auth_headers,
    test_product,
    test_supplier,
):

    response = client.post(
        "/purchase-orders",
        headers=auth_headers,
        json={
            "supplier_id": test_supplier["id"],
            "notes": "First purchase order",
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": 10,
                    "unit_price": 5,
                }
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["supplier_id"] == test_supplier["id"]

    assert data["status"] == "draft"

    assert data["notes"] == "First purchase order"

    assert len(data["items"]) == 1

    item = data["items"][0]

    assert item["product_id"] == test_product["id"]

    assert item["quantity"] == 10

    assert float(item["unit_price"]) == 5

    assert float(item["total_price"]) == 50

    assert float(data["total_amount"]) == 50