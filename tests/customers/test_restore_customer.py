def test_restore_customer(client):
    create_payload = {
        "full_name": "Ali Ahmadi",
        "phone": "09120000005",
        "email": "ali5@example.com",
        "birthday": "1995-05-20",
        "address": "Tehran",
        "gender": "MALE",
    }

    create_response = client.post(
        "/customers",
        json=create_payload,
    )

    assert create_response.status_code == 201

    customer_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/customers/{customer_id}",
    )

    assert delete_response.status_code == 200

    deleted_customer = delete_response.json()

    assert deleted_customer["id"] == customer_id
    assert deleted_customer["is_deleted"] is True
    assert deleted_customer["is_active"] is False

    restore_response = client.patch(
        f"/customers/{customer_id}/restore",
    )

    assert restore_response.status_code == 200

    restored_customer = restore_response.json()

    assert restored_customer["id"] == customer_id
    assert restored_customer["is_deleted"] is False
    assert restored_customer["is_active"] is True