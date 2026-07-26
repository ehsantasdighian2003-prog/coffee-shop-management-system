def test_protected_route_without_token(client):

    response = client.post(
        "/products/",
        json={
            "name": "Test Coffee",
            "description": "Security Test",
            "price": 5,
            "stock": 10,
            "is_active": True
        }
    )

    assert response.status_code == 401



def test_protected_route_invalid_token(client):

    response = client.post(
        "/products/",
        headers={
            "Authorization": "Bearer invalid_token"
        },
        json={
            "name": "Test Coffee",
            "description": "Security Test",
            "price": 5,
            "stock": 10,
            "is_active": True
        }
    )

    assert response.status_code == 401



def test_protected_route_with_valid_token(
    client,
    admin_token,
    test_category
):

    response = client.post(
        "/products/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Security Coffee",
            "description": "Valid Token Test",
            "price": 5,
            "stock": 10,
            "is_active": True,
            "category_id": test_category["id"]
        }
    )


    assert response.status_code == 201



def test_admin_route_with_user_token(
    client,
    user_token
):

    response = client.post(
        "/products/",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "name": "User Coffee",
            "description": "RBAC Test",
            "price": 5,
            "stock": 10,
            "is_active": True
        }
    )


    assert response.status_code == 403