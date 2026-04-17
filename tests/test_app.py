import pytest

import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app


@pytest.fixture
def asgi_transport():
    return ASGITransport(app=app)

@pytest.mark.asyncio
async def test_get_activities(asgi_transport):
    # Arrange
    # (No setup needed for in-memory data)

    # Act
    async with AsyncClient(transport=asgi_transport, base_url="http://test") as ac:
        response = await ac.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_and_unregister(asgi_transport):
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    async with AsyncClient(transport=asgi_transport, base_url="http://test") as ac:
        # Act: Sign up
        signup_resp = await ac.post(f"/activities/{activity}/signup?email={email}")
        # Assert
        assert signup_resp.status_code == 200
        assert f"Signed up {email}" in signup_resp.json()["message"]

        # Act: Unregister
        unregister_resp = await ac.delete(f"/activities/{activity}/participants?email={email}")
        # Assert
        assert unregister_resp.status_code == 200
        assert f"Unregistered {email}" in unregister_resp.json()["message"]

        # Act: Unregister again (should fail)
        unregister_resp2 = await ac.delete(f"/activities/{activity}/participants?email={email}")
        # Assert
        assert unregister_resp2.status_code == 404
        assert "not signed up" in unregister_resp2.json()["detail"].lower()
