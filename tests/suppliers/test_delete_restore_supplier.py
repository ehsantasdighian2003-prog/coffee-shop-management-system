def test_delete_restore_supplier(client, auth_headers):

    create_response = client.post(
        "/suppliers/",
        headers=auth_headers,
        json={
            "name": "Delete Supplier",
            "phone": "09444444444",
            "email": "delete@test.com",
            "address": "Tehran",
        },
    )

    assert create_response.status_code == 201

    supplier_id = create_response.json()["id"]


    # Delete

    delete_response = client.delete(
        f"/suppliers/{supplier_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 200

    delete_data = delete_response.json()

    assert delete_data["id"] == supplier_id


    # Restore

    restore_response = client.patch(
        f"/suppliers/{supplier_id}/restore",
        headers=auth_headers,
    )

    assert restore_response.status_code == 200

    restore_data = restore_response.json()

    assert restore_data["id"] == supplier_id
    assert restore_data["is_deleted"] is False