def test_activate_deactivate_supplier(client, auth_headers):

    create_response = client.post(
        "/suppliers/",
        headers=auth_headers,
        json={
            "name": "Status Supplier",
            "phone": "09333333333",
            "email": "status@test.com",
            "address": "Tehran",
        },
    )

    assert create_response.status_code == 201

    supplier_id = create_response.json()["id"]

    # Deactivate

    deactivate_response = client.patch(
        f"/suppliers/{supplier_id}/deactivate",
        headers=auth_headers,
    )

    assert deactivate_response.status_code == 200

    deactivate_data = deactivate_response.json()

    assert deactivate_data["is_active"] is False


    # Activate

    activate_response = client.patch(
        f"/suppliers/{supplier_id}/activate",
        headers=auth_headers,
    )

    assert activate_response.status_code == 200

    activate_data = activate_response.json()

    assert activate_data["is_active"] is True