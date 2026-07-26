def test_update_category(
    client,
    auth_headers,
    test_category
):

    response = client.put(
        f"/categories/{test_category['id']}",
        headers=auth_headers,
        json={
            "name": "Hot Coffee"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == test_category["id"]
    assert data["name"] == "Hot Coffee"
    
    
def test_update_category_without_token(
    client,
    test_category
):

    response = client.put(
        f"/categories/{test_category['id']}",
        json={
            "name": "Hot Coffee"
        }
    )

    assert response.status_code == 401
    
    
def test_update_category_as_user(
    client,
    user_token,
    test_category
):

    response = client.put(
        f"/categories/{test_category['id']}",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "name": "Hot Coffee"
        }
    )

    assert response.status_code == 403
    
    
def test_update_category_not_found(
    client,
    auth_headers
):

    response = client.put(
        "/categories/9999",
        headers=auth_headers,
        json={
            "name": "Hot Coffee"
        }
    )

    assert response.status_code == 404