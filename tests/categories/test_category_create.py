def test_create_category(client, auth_headers):
    response = client.post(
        "/categories/",
        headers=auth_headers,
        json={
            "name": "Coffee"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["name"] == "Coffee"
    
    
def test_create_category_without_token(client):
    response = client.post(
        "/categories/",
        json={
            "name": "Coffee"
        }
    )

    assert response.status_code == 401