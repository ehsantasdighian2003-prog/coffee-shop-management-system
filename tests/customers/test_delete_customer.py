from uuid import UUID


def test_delete_customer(client):
    create_payload = {
        "full_name": "Ali Ahmadi",
        "phone": "09120000004",
        "email": "ali4@example.com",
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

    # verify customer is no longer accessible
    get_response = client.get(
        f"/customers/{customer_id}",
    )

    assert get_response.status_code == 404