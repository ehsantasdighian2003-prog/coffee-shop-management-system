def test_update_supplier(client, auth_headers):

    create_response = client.post(
        "/suppliers/",
        headers=auth_headers,
        json={
            "name": "Old Supplier",
            "phone": "09111111111",
            "email": "old@test.com",
            "address": "Old Address",
        },
    )

    assert create_response.status_code == 201

    supplier_id = create_response.json()["id"]

    response = client.put(
        f"/suppliers/{supplier_id}",
        headers=auth_headers,
        json={
            "name": "Updated Supplier",
            "phone": "09222222222",
            "email": "updated@test.com",
            "address": "New Address",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == supplier_id
    assert data["name"] == "Updated Supplier"
    assert data["phone"] == "09222222222"
    assert data["email"] == "updated@test.com"
    assert data["address"] == "New Address"