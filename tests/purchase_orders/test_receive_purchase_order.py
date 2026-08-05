def test_receive_purchase_order(
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
            "notes": "Coffee beans purchase",
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": 20,
                    "unit_price": 5,
                }
            ],
        },
    )

    assert response.status_code == 200

    purchase_order = response.json()

    purchase_order_id = purchase_order["id"]


    # =========================
    # GET INITIAL STOCK
    # =========================

    product_response = client.get(
        f"/products/{test_product['id']}",
        headers=auth_headers,
    )

    assert product_response.status_code == 200

    initial_stock = product_response.json()["stock"]


    # =========================
    # RECEIVE PURCHASE ORDER
    # =========================

    response = client.put(
        f"/purchase-orders/{purchase_order_id}/receive",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()


    # =========================
    # CHECK STATUS
    # =========================

    assert data["status"] == "received"


    # =========================
    # CHECK STOCK INCREASE
    # =========================

    product_response = client.get(
        f"/products/{test_product['id']}",
        headers=auth_headers,
    )

    product = product_response.json()

    assert product["stock"] == initial_stock + 20