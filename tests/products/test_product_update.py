def test_update_product(
    client,
    auth_headers,
    test_product
):

    product_id = test_product["id"]


    response = client.put(
        f"/products/{product_id}",
        headers=auth_headers,
        json={
            "name": "Updated Espresso",
            "price": 7,
            "stock": 50
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["id"] == product_id
    assert data["name"] == "Updated Espresso"
    assert data["price"] == 7
    assert data["stock"] == 50