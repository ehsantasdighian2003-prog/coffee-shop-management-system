import pytest


def test_create_customer(client):
    payload = {
        "full_name": "Ali Ahmadi",
        "phone": "09120000001",
        "email": "ali@example.com",
        "birthday": "1995-05-20",
        "address": "Tehran",
        "gender": "MALE",
    }

    response = client.post(
        "/customers",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["full_name"] == "Ali Ahmadi"
    assert data["phone"] == "09120000001"
    assert data["email"] == "ali@example.com"
    assert data["status"] == "ACTIVE"
    assert data["loyalty_points"] == 0
    assert data["membership_level"] == "BRONZE"
    assert data["is_active"] is True