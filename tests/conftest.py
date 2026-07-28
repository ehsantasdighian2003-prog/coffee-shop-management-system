import os

os.environ["DATABASE_NAME"] = "coffee_shop_test"


import pytest
from fastapi.testclient import TestClient

from app.core.database import get_connection
from app.main import app
from tests.fixtures.orders import *

# =====================================================
# CLEAN TEST DATABASE BEFORE EACH TEST
# =====================================================


@pytest.fixture(autouse=True)
def clean_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        TRUNCATE TABLE
            order_items,
            orders,
            products,
            categories,
            users
        RESTART IDENTITY
        CASCADE;
        """)

    conn.commit()

    cursor.close()
    conn.close()


# =====================================================
# TEST CLIENT
# =====================================================


@pytest.fixture
def client():

    return TestClient(app)


# =====================================================
# CREATE ADMIN USER AND GET JWT TOKEN
# =====================================================


@pytest.fixture
def admin_token(client):

    register_response = client.post(
        "/auth/register",
        json={
            "username": "admin_test",
            "email": "admin@test.com",
            "password": "12345678",
        },
    )

    assert register_response.status_code == 201, register_response.json()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET role = 'admin'
        WHERE username = 'admin_test';
        """)

    conn.commit()

    cursor.close()
    conn.close()

    login_response = client.post(
        "/auth/login", json={"username": "admin_test", "password": "12345678"}
    )

    assert login_response.status_code == 200, login_response.json()

    return login_response.json()["access_token"]


# =====================================================
# AUTH HEADERS
# =====================================================


@pytest.fixture
def auth_headers(admin_token):

    return {"Authorization": f"Bearer {admin_token}"}


# =====================================================
# CREATE TEST USER
# =====================================================


@pytest.fixture
def test_user(client):

    response = client.post(
        "/auth/register",
        json={
            "username": "test_user",
            "email": "test_user@test.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 201, response.json()

    return {"username": "test_user", "password": "12345678"}


# =====================================================
# CREATE NORMAL USER TOKEN
# =====================================================


@pytest.fixture
def user_token(client, test_user):

    login_response = client.post(
        "/auth/login",
        json={"username": test_user["username"], "password": test_user["password"]},
    )

    assert login_response.status_code == 200, login_response.json()

    return login_response.json()["access_token"]


# =====================================================
# CREATE TEST CATEGORY
# =====================================================


@pytest.fixture
def test_category(client, auth_headers):

    response = client.post(
        "/categories/", headers=auth_headers, json={"name": "Coffee"}
    )

    assert response.status_code == 201, response.json()

    return response.json()


# =====================================================
# CREATE TEST PRODUCT
# =====================================================


@pytest.fixture
def test_product(client, auth_headers, test_category):

    response = client.post(
        "/products/",
        headers=auth_headers,
        json={
            "name": "Espresso",
            "description": "Hot coffee",
            "price": 5.5,
            "stock": 100,
            "is_active": True,
            "category_id": test_category["id"],
        },
    )

    assert response.status_code == 201, response.json()

    return response.json()
