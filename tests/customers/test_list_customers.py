def test_list_customers(client):
    customer_1 = {
        "full_name": "Ali Ahmadi",
        "phone": "09120000006",
        "email": "ali6@example.com",
        "birthday": "1995-05-20",
        "address": "Tehran",
        "gender": "MALE",
    }

    customer_2 = {
        "full_name": "Sara Ahmadi",
        "phone": "09120000007",
        "email": "sara7@example.com",
        "birthday": "1998-03-15",
        "address": "Shiraz",
        "gender": "FEMALE",
    }

    response_1 = client.post(
        "/customers",
        json=customer_1,
    )

    response_2 = client.post(
        "/customers",
        json=customer_2,
    )

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    response = client.get(
        "/customers",
    )

    assert response.status_code == 200

    customers = response.json()

    assert isinstance(customers, list)
    assert len(customers) >= 2

    customer_ids = [
        customer["id"]
        for customer in customers
    ]

    assert response_1.json()["id"] in customer_ids
    assert response_2.json()["id"] in customer_ids