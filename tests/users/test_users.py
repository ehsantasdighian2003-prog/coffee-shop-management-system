def create_test_user(client):

    response = client.post(
        "/auth/register",
        json={
            "username": "user_test_1",
            "password": "password123",
            "first_name": "User",
            "last_name": "Test",
            "email": "user_test_1@example.com",
        },
    )

    assert response.status_code == 201

    return response.json()["user_id"]


# ==================================================
# GET USER BY ID
# ==================================================


def test_get_user_by_id(client):

    user_id = create_test_user(client)

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["username"] == "user_test_1"


# ==================================================
# GET USERS LIST
# ==================================================


def test_get_users(client):

    create_test_user(client)

    response = client.get("/users/")

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert "meta" in data

    assert data["meta"]["total"] >= 1


# ==================================================
# GET USER NOT FOUND
# ==================================================


def test_get_user_not_found(client):

    response = client.get("/users/999999")

    assert response.status_code == 404


# ==================================================
# UPDATE USER PROFILE
# ==================================================


def test_update_user_profile(client):

    user_id = create_test_user(client)

    response = client.put(
        f"/users/{user_id}",
        json={
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated_user@example.com",
            "phone_number": "09120000000",
            "profile_image": "profile.png",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "User"
    assert data["email"] == "updated_user@example.com"


# ==================================================
# CHANGE PASSWORD
# ==================================================


def test_change_password(client):

    user_id = create_test_user(client)

    response = client.patch(
        f"/users/{user_id}/password",
        json={
            "old_password": "password123",
            "new_password": "newpassword123",
        },
    )

    assert response.status_code == 200

    # login with new password

    login_response = client.post(
        "/auth/login",
        json={
            "username": "user_test_1",
            "password": "newpassword123",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data


def test_update_user_role(client):

    user_id = create_test_user(client)

    response = client.patch(
        f"/users/{user_id}/role",
        json={"role": "admin"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["role"] == "admin"


def test_deactivate_user(client):

    user_id = create_test_user(client)

    response = client.patch(f"/users/{user_id}/deactivate")

    assert response.status_code == 200

    data = response.json()

    assert data["is_active"] is False


def test_activate_user(client):

    user_id = create_test_user(client)

    # deactivate first
    client.patch(f"/users/{user_id}/deactivate")

    response = client.patch(f"/users/{user_id}/activate")

    assert response.status_code == 200

    data = response.json()

    assert data["is_active"] is True


def test_soft_delete_user(client):

    user_id = create_test_user(client)

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["deleted_at"] is not None
    assert data["is_active"] is False


def test_restore_user(client):

    user_id = create_test_user(client)

    # delete first
    client.delete(f"/users/{user_id}")

    response = client.patch(f"/users/{user_id}/restore")

    assert response.status_code == 200

    data = response.json()

    assert data["deleted_at"] is None
    assert data["is_active"] is True
