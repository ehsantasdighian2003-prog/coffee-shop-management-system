def test_delete_product(
    client,
    auth_headers,
    test_product
):

    product_id = test_product["id"]


    response = client.delete(
        f"/products/{product_id}",
        headers=auth_headers
    )


    assert response.status_code == 200


    data = response.json()

    assert data["id"] == product_id
    
def test_deleted_product_not_found(
    client,
    auth_headers,
    test_product
):

    product_id = test_product["id"]


    client.delete(
        f"/products/{product_id}",
        headers=auth_headers
    )


    response = client.get(
        f"/products/{product_id}",
        headers=auth_headers
    )


    assert response.status_code == 404