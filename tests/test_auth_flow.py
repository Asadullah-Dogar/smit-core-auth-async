import pytest
from httpx import AsyncClient

# We use a standard test user
TEST_USER = {
    "email": "test@example.com",
    "password": "SecurePassword123!"
}

@pytest.mark.asyncio
async def test_end_to_end_auth_sequence(async_client: AsyncClient):
    """Executes the exact 6-step verification blueprint from the spec."""
    
    # --- 1. The Registration Step ---
    reg_response = await async_client.post("/auth/register", json=TEST_USER)
    assert reg_response.status_code == 201
    data = reg_response.json()
    assert data["email"] == TEST_USER["email"]
    assert "id" in data
    assert "password" not in data  # Ensure password is NEVER returned
    
    # --- 2. The Authentication Step ---
    login_response = await async_client.post("/auth/login", json=TEST_USER)
    assert login_response.status_code == 200
    tokens = login_response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"
    
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    
    # --- 3. The Security Access Step ---
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_response = await async_client.get("/users/me", headers=headers)
    assert profile_response.status_code == 200
    assert profile_response.json()["email"] == TEST_USER["email"]
    
    # --- 4. The Rotation Step ---
    refresh_headers = {"refresh-token": refresh_token}
    rotation_response = await async_client.post("/tokens/refresh", headers=refresh_headers)
    assert rotation_response.status_code == 200
    new_tokens = rotation_response.json()
    assert "access_token" in new_tokens
    
    new_access_token = new_tokens["access_token"]
    
    # --- 5. The Session Revocation Step (Logout) ---
    logout_headers = {"access-token": new_access_token}
    logout_response = await async_client.post("/tokens/logout", headers=logout_headers)
    assert logout_response.status_code == 200
    assert logout_response.json()["detail"] == "Revocation complete"
    
    # --- 6. The Zero-Trust Post-Validation Step ---
    # Attempting to use the revoked token to access the protected route
    blocked_headers = {"Authorization": f"Bearer {new_access_token}"}
    blocked_response = await async_client.get("/users/me", headers=blocked_headers)
    assert blocked_response.status_code == 401
    assert "revoked" in blocked_response.json()["detail"].lower()