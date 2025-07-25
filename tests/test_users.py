import pytest

@pytest.mark.asyncio
async def test_create_client(async_client):
    response = await async_client.post(
        "/clients/",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890",
            "telegram_id": 12345
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
