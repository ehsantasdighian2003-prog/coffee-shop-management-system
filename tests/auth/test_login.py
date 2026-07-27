def test_login_success(client, test_user):

    response = client.post(
        "/auth/login",
        json={"username": test_user["username"], "password": test_user["password"]},
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):

    response = client.post(
        "/auth/login",
        json={"username": test_user["username"], "password": "wrong_password"},
    )

    assert response.status_code == 401


def test_login_invalid_username(client):

    response = client.post(
        "/auth/login", json={"username": "unknown_user", "password": "12345678"}
    )

    assert response.status_code == 401
