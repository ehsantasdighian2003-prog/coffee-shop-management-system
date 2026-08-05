def test_create_warehouse(
    client,
    auth_headers,
):

    response = client.post(
        "/warehouses/",
        headers=auth_headers,
        json={
            "name": "Main Warehouse",
            "location": "Tehran",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Main Warehouse"
    assert data["location"] == "Tehran"