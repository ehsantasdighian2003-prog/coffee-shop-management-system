from fastapi import status


def test_register_success(client):

    response = client.post(
        "/auth/register",
        json={
            "username": "new_user",
            "email": "new_user@test.com",
            "password": "12345678",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["message"] == "User registered successfully."
    assert isinstance(data["user_id"], int)


def test_register_duplicate_email(client):

    first_response = client.post(
        "/auth/register",
        json={
            "username": "user_one",
            "email": "same@test.com",
            "password": "12345678",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json={
            "username": "user_two",
            "email": "same@test.com",
            "password": "12345678",
        },
    )

    assert second_response.status_code in (400, 409)
