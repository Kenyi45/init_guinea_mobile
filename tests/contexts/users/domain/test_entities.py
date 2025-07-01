import pytest
from src.contexts.users.domain.entities import User, UserCreated, UserUpdated
from src.contexts.users.domain.value_objects import Email, Username, FullName, HashedPassword


class TestUser:
    """Test cases for User entity."""
    
    def test_create_user_factory_method(self):
        """Test creating user using factory method."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password="$2b$12$hashed_value"
        )
        
        assert user.email.value == "test@example.com"
        assert user.username.value == "testuser"
        assert user.full_name.first_name == "Test"
        assert user.full_name.last_name == "User"
        assert user.full_name.full_name == "Test User"
        assert user.hashed_password.hashed_value == "$2b$12$hashed_value"
        assert user.is_active is True
        assert user.id is not None
        assert user.created_at is not None
        assert user.updated_at is not None
    
    def test_create_user_generates_domain_event(self):
        """Test creating user generates UserCreated domain event."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password="$2b$12$hashed_value"
        )
        
        events = user.get_domain_events()
        assert len(events) == 1
        assert isinstance(events[0], UserCreated)
        assert events[0].event_type == "user_created"
        assert events[0].data["user_id"] == user.id
        assert events[0].data["email"] == "test@example.com"
        assert events[0].data["username"] == "testuser"
    
    def test_update_profile(self):
        """Test updating user profile."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password="$2b$12$hashed_value"
        )
        
        # Clear initial events
        user.clear_domain_events()
        
        user.update_profile(first_name="Updated", last_name="Name")
        
        assert user.full_name.first_name == "Updated"
        assert user.full_name.last_name == "Name"
        assert user.full_name.full_name == "Updated Name"
        
        # Check domain event was generated
        events = user.get_domain_events()
        assert len(events) == 1
        assert isinstance(events[0], UserUpdated)
        assert events[0].event_type == "user_updated"
        assert events[0].data["user_id"] == user.id
        assert "full_name" in events[0].data["changes"]
    
    def test_update_profile_partial(self):
        """Test updating user profile partially."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password="$2b$12$hashed_value"
        )
        
        user.clear_domain_events()
        
        user.update_profile(first_name="Updated")
        
        assert user.full_name.first_name == "Updated"
        assert user.full_name.last_name == "User"  # Should remain unchanged
    
    def test_deactivate_user(self):
        """Test deactivating user."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password="$2b$12$hashed_value"
        )
        
        user.clear_domain_events()
        
        user.deactivate()
        
        assert user.is_active is False
        
        # Check domain event was generated
        events = user.get_domain_events()
        assert len(events) == 1
        assert isinstance(events[0], UserUpdated)
        assert events[0].data["changes"]["is_active"] is False
    
    def test_activate_user(self):
        """Test activating user."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password="$2b$12$hashed_value"
        )
        
        user.deactivate()
        user.clear_domain_events()
        
        user.activate()
        
        assert user.is_active is True
        
        # Check domain event was generated
        events = user.get_domain_events()
        assert len(events) == 1
        assert isinstance(events[0], UserUpdated)
        assert events[0].data["changes"]["is_active"] is True
    
    def test_user_equality(self):
        """Test user equality comparison."""
        user1 = User.create(
            email="test1@example.com",
            username="testuser1",
            first_name="Test",
            last_name="User",
            hashed_password="$2b$12$hashed_value"
        )
        
        user2 = User.create(
            email="test2@example.com",
            username="testuser2",
            first_name="Test",
            last_name="User",
            hashed_password="$2b$12$hashed_value"
        )
        
        # Create user with same ID as user1
        user3 = User(user_id=user1.id)
        
        assert user1 != user2  # Different IDs
        assert user1 == user3   # Same ID
    
    def test_user_hash(self):
        """Test user hash method."""
        user1 = User.create(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password="$2b$12$hashed_value"
        )
        
        user2 = User(user_id=user1.id)
        
        assert hash(user1) == hash(user2)  # Same ID should have same hash
    
    def test_clear_domain_events(self):
        """Test clearing domain events."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password="$2b$12$hashed_value"
        )
        
        assert len(user.get_domain_events()) == 1
        
        user.clear_domain_events()
        
        assert len(user.get_domain_events()) == 0 