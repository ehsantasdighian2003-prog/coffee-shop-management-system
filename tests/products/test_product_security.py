def test_create_product_without_token(client):

    response = client.post(
        "/products/",
        json={
            "name": "No Token Product",
            "description": "Security Test",
            "price": 10,
            "stock": 5,
            "is_active": True,
            "category_id": 1
        }
    )

    assert response.status_code == 401
    
    
def test_create_product_with_invalid_token(client):

    response = client.post(
        "/products/",
        headers={
            "Authorization": "Bearer invalid_token"
        },
        json={
            "name": "Invalid Token Product",
            "description": "Security Test",
            "price": 10,
            "stock": 5,
            "is_active": True,
            "category_id": 1
        }
    )

    assert response.status_code == 401
    
    
def test_create_product_with_user_role(
    client,
    user_token
):

    response = client.post(
        "/products/",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "name": "User Product",
            "description": "Permission Test",
            "price": 10,
            "stock": 5,
            "is_active": True,
            "category_id": 1
        }
    )

    assert response.status_code == 403