def test_get_suppliers(client, auth_headers):

    create_response = client.post(
        "/suppliers/",
        headers=auth_headers,
        json={
            "name": "Test Supplier",
            "phone": "09111111111",
            "email": "supplier@test.com",
            "address": "Tehran",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/suppliers/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert "meta" in data

    assert data["meta"]["total"] >= 1

    assert data["data"][0]["name"] == "Test Supplier"