def test_get_customer(client):
    create_payload = {
        "full_name": "Ali Ahmadi",
        "phone": "09120000002",
        "email": "ali2@example.com",
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

    response = client.get(
        f"/customers/{customer_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == customer_id
    assert data["full_name"] == "Ali Ahmadi"
    assert data["phone"] == "09120000002"