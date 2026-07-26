def test_get_product_by_id(
    client,
    auth_headers,
    test_product
):

    product_id = test_product["id"]


    response = client.get(
        f"/products/{product_id}",
        headers=auth_headers
    )


    assert response.status_code == 200


    data = response.json()


    assert data["id"] == product_id
    assert data["name"] == "Espresso"
    assert data["stock"] == 100