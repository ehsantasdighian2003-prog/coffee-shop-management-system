def test_delete_category(client, auth_headers, test_category):

    response = client.delete(f"/categories/{test_category['id']}", headers=auth_headers)

    assert response.status_code == 200

    data = response.json()

    assert data["category_id"] == test_category["id"]


def test_delete_category_without_token(client, test_category):

    response = client.delete(f"/categories/{test_category['id']}")

    assert response.status_code == 401


def test_delete_category_as_user(client, user_token, test_category):

    response = client.delete(
        f"/categories/{test_category['id']}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 403


def test_delete_category_not_found(client, auth_headers):

    response = client.delete("/categories/9999", headers=auth_headers)

    assert response.status_code == 404


def test_deleted_category_not_found(client, auth_headers, test_category):

    category_id = test_category["id"]

    client.delete(f"/categories/{category_id}", headers=auth_headers)

    response = client.get(f"/categories/{category_id}")

    assert response.status_code == 404
