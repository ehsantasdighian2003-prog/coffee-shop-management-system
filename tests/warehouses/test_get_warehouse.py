def test_get_warehouse(
    client,
    auth_headers,
):

    create_response = client.post(
        "/warehouses",
        headers=auth_headers,
        json={
            "name": "Main Warehouse",
            "location": "Tehran",
        },
    )

    assert create_response.status_code == 201

    warehouse = create_response.json()

    warehouse_id = warehouse["id"]

    response = client.get(
        f"/warehouses/{warehouse_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == warehouse_id
    assert data["name"] == "Main Warehouse"
    assert data["location"] == "Tehran"
    assert data["is_active"] is True