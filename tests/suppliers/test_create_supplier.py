def test_create_supplier(client, auth_headers):

    response = client.post(
        "/suppliers/",
        headers=auth_headers,
        json={
            "name": "Arabica Supplier",
            "phone": "09123456789",
            "email": "arabica@test.com",
            "address": "Tehran",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Arabica Supplier"
    assert data["phone"] == "09123456789"
    assert data["email"] == "arabica@test.com"
    assert data["is_active"] is True
    assert data["is_deleted"] is False