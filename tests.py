import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app  # Импортируйте ваше приложение из main.py
import pytest_asyncio

# Инициализация клиента для тестирования FastAPI приложения
@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_signup(async_client):
    # Тест регистрации нового пользователя
    response = await async_client.post("/signup", data={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 200
    assert response.json() == {"message": "Пользователь успешно зарегистрирован"}

@pytest.mark.asyncio
async def test_duplicate_signup(async_client):
    # Тест на попытку зарегистрировать пользователя с уже существующим именем
    response = await async_client.post("/signup", data={
        "username": "alice",  # Имя пользователя, которое уже существует
        "email": "alice2@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Пользователь с таким именем уже существует"}

@pytest.mark.asyncio
async def test_login(async_client):
    # Тест входа существующего пользователя
    response = await async_client.post("/token", data={
        "username": "alice",
        "password": "alicepassword"  # Правильный пароль для alice
    })

    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_invalid_login(async_client):
    # Тест входа с неправильным паролем
    response = await async_client.post("/token", data={
        "username": "alice",
        "password": "wrongpassword"  # Неправильный пароль
    })

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect username or password"
    }

@pytest.mark.asyncio
async def test_get_current_user(async_client):
    # Сначала получаем токен для входа
    login_response = await async_client.post("/token", data={
        "username": "alice",
        "password": "alicepassword"
    })
    token = login_response.json()["access_token"]

    # Используем полученный токен для запроса данных текущего пользователя
    response = await async_client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == "alice"
    assert user_data["email"] == "alice@example.com"
