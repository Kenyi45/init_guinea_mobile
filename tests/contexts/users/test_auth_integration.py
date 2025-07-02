import pytest
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


class TestAuthIntegration:
    """Test integration between auth and user endpoints."""
    
    def test_create_user_public_endpoint(self, db_session):
        """Test that user creation doesn't require authentication."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestPassword123!"
        }
        
        response = client.post("/api/v1/users", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "id" in data
    
    def test_protected_endpoints_require_auth(self, db_session):
        """Test that protected endpoints require JWT token."""
        # Try to access protected endpoints without token
        endpoints = [
            ("GET", "/api/v1/users"),
            ("GET", "/api/v1/users/some-id"),
            ("PUT", "/api/v1/users/some-id"),
            ("DELETE", "/api/v1/users/some-id")
        ]
        
        for method, endpoint in endpoints:
            response = client.request(method, endpoint)
            assert response.status_code == 403  # Forbidden without auth
    
    def test_full_auth_flow(self, db_session):
        """Test complete authentication flow."""
        # 1. Create user
        user_data = {
            "email": "authtest@example.com",
            "username": "authtest",
            "first_name": "Auth",
            "last_name": "Test",
            "password": "AuthPassword123!"
        }
        
        response = client.post("/api/v1/users", json=user_data)
        assert response.status_code == 200
        user = response.json()
        user_id = user["id"]
        
        # 2. Login
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        
        auth_data = response.json()
        assert "access_token" in auth_data
        token = auth_data["access_token"]
        
        # 3. Use token to access protected endpoints
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get user
        response = client.get(f"/api/v1/users/{user_id}", headers=headers)
        assert response.status_code == 200
        
        # List users
        response = client.get("/api/v1/users", headers=headers)
        assert response.status_code == 200
        
        # Update user
        update_data = {"first_name": "Updated", "last_name": "Name"}
        response = client.put(f"/api/v1/users/{user_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        
        # Refresh token
        response = client.post("/api/v1/auth/refresh", headers=headers)
        assert response.status_code == 200
        refresh_data = response.json()
        assert "access_token" in refresh_data
        new_token = refresh_data["access_token"]
        assert new_token != token  # Token should be different
        
        # Delete user
        response = client.delete(f"/api/v1/users/{user_id}", headers=headers)
        assert response.status_code == 204  # No content
    
    def test_invalid_token_access(self, db_session):
        """Test that invalid tokens are rejected."""
        headers = {"Authorization": "Bearer invalid-token"}
        
        response = client.get("/api/v1/users", headers=headers)
        assert response.status_code == 401  # Unauthorized
        
        response_data = response.json()
        assert "Invalid authentication credentials" in response_data["detail"]
    
    def test_expired_token_refresh(self, db_session):
        """Test refreshing an expired token."""
        # This would require mocking time or using a very short expiration
        # For now, test with a malformed token
        headers = {"Authorization": "Bearer expired.token.here"}
        
        response = client.post("/api/v1/auth/refresh", headers=headers)
        assert response.status_code == 401
    
    def test_verify_token_endpoint(self, db_session):
        """Test token verification endpoint."""
        # Create user and login to get valid token
        user_data = {
            "email": "verify@example.com",
            "username": "verifyuser",
            "first_name": "Verify",
            "last_name": "User",
            "password": "VerifyPassword123!"
        }
        
        client.post("/api/v1/users", json=user_data)
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        token = login_response.json()["access_token"]
        
        # Verify valid token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/api/v1/auth/verify", headers=headers)
        assert response.status_code == 200
        
        verify_data = response.json()
        assert verify_data["valid"] is True
        assert "user_id" in verify_data
        assert verify_data["email"] == user_data["email"]
        
        # Verify invalid token
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.post("/api/v1/auth/verify", headers=headers)
        assert response.status_code == 401 