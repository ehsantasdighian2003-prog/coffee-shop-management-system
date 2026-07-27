def test_get_category_by_id(client, test_category):

    response = client.get(f"/categories/{test_category['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == test_category["id"]
    assert data["name"] == "Coffee"


def test_get_category_not_found(client):

    response = client.get("/categories/9999")

    assert response.status_code == 404


def test_get_all_categories(client, test_category):

    response = client.get("/categories/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]["name"] == "Coffee"