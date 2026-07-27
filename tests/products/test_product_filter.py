def create_category(client, admin_token):

    response = client.post(
        "/categories/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Test Category", "description": "Category For Testing"},
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_product(client, admin_token, name, category_id, price=10, stock=10):

    response = client.post(
        "/products/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": name,
            "description": "Filter Test Product",
            "price": price,
            "stock": stock,
            "is_active": True,
            "category_id": category_id,
        },
    )

    assert response.status_code == 201

    return response.json()


# =====================================================
# SEARCH
# =====================================================


def test_search_products(client, admin_token):

    category_id = create_category(client, admin_token)

    create_product(client, admin_token, "Coffee Espresso", category_id)

    create_product(client, admin_token, "Green Tea", category_id)

    response = client.get("/products/?search=Coffee")

    assert response.status_code == 200

    data = response.json()

    assert len(data["data"]) >= 1

    assert "Coffee" in data["data"][0]["name"]


# =====================================================
# PAGINATION
# =====================================================


def test_products_pagination(client, admin_token):

    category_id = create_category(client, admin_token)

    for i in range(15):

        create_product(client, admin_token, f"Product {i}", category_id)

    response = client.get("/products/?page=1&limit=10")

    assert response.status_code == 200

    data = response.json()

    assert len(data["data"]) == 10
    assert data["meta"]["page"] == 1
    assert data["meta"]["limit"] == 10
    assert data["meta"]["total"] >= 15


# =====================================================
# FILTER BY CATEGORY
# =====================================================


def test_filter_products_by_category(client, admin_token):

    category_id = create_category(client, admin_token)

    create_product(client, admin_token, "Coffee", category_id)

    create_product(client, admin_token, "Latte", category_id)

    response = client.get(f"/products/?category_id={category_id}")

    assert response.status_code == 200

    data = response.json()

    assert len(data["data"]) >= 2

    for product in data["data"]:
        assert product["category_id"] == category_id
