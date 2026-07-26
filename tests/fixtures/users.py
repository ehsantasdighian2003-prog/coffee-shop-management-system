import pytest

from app.schemas.auth import UserRegister
from app.services.auth_service import AuthService


@pytest.fixture
def auth_service():

    return AuthService()


@pytest.fixture
def test_user(auth_service):

    user_data = UserRegister(
        username="pytest_user",
        password="password123",
        first_name="Pytest",
        last_name="User",
        email="pytest@example.com",
    )

    return auth_service.register(
        user_data
    )