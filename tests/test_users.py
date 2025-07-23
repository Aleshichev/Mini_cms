import pytest


@pytest.mark.asyncio
async def test_create_user(async_client):
    response = await async_client.post(
        "/user/",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "telegram_id": 12345678,
            "role": "manager",
            "hashed_password": "pA1ssword",
        },
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "manager"
    assert data["full_name"] == "Test User"
    assert data["telegram_id"] == 12345678
