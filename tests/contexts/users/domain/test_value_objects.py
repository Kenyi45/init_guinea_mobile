import pytest
from src.contexts.users.domain.value_objects import Email, Username, FullName, HashedPassword
from src.shared.domain.exceptions import ValidationError


class TestEmail:
    """Test cases for Email value object."""
    
    def test_valid_email(self):
        """Test creating email with valid format."""
        email = Email("test@example.com")
        assert email.value == "test@example.com"
    
    def test_email_lowercase_conversion(self):
        """Test email is converted to lowercase."""
        email = Email("TEST@EXAMPLE.COM")
        assert email.value == "test@example.com"
    
    def test_invalid_email_format(self):
        """Test creating email with invalid format raises ValidationError."""
        with pytest.raises(ValidationError):
            Email("invalid-email")
        
        with pytest.raises(ValidationError):
            Email("test@")
        
        with pytest.raises(ValidationError):
            Email("@example.com")
    
    def test_email_equality(self):
        """Test email equality comparison."""
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        email3 = Email("other@example.com")
        
        assert email1 == email2
        assert email1 != email3


class TestUsername:
    """Test cases for Username value object."""
    
    def test_valid_username(self):
        """Test creating username with valid format."""
        username = Username("testuser123")
        assert username.value == "testuser123"
    
    def test_username_too_short(self):
        """Test username too short raises ValidationError."""
        with pytest.raises(ValidationError):
            Username("ab")
    
    def test_username_too_long(self):
        """Test username too long raises ValidationError."""
        with pytest.raises(ValidationError):
            Username("a" * 51)
    
    def test_username_invalid_characters(self):
        """Test username with invalid characters raises ValidationError."""
        with pytest.raises(ValidationError):
            Username("test-user")
        
        with pytest.raises(ValidationError):
            Username("test user")
        
        with pytest.raises(ValidationError):
            Username("test@user")
    
    def test_username_equality(self):
        """Test username equality comparison."""
        username1 = Username("testuser")
        username2 = Username("testuser")
        username3 = Username("otheruser")
        
        assert username1 == username2
        assert username1 != username3


class TestFullName:
    """Test cases for FullName value object."""
    
    def test_valid_full_name(self):
        """Test creating full name with valid values."""
        full_name = FullName("John", "Doe")
        assert full_name.first_name == "John"
        assert full_name.last_name == "Doe"
        assert full_name.full_name == "John Doe"
    
    def test_full_name_with_whitespace(self):
        """Test full name strips whitespace."""
        full_name = FullName("  John  ", "  Doe  ")
        assert full_name.first_name == "John"
        assert full_name.last_name == "Doe"
    
    def test_empty_first_name(self):
        """Test empty first name raises ValidationError."""
        with pytest.raises(ValidationError):
            FullName("", "Doe")
        
        with pytest.raises(ValidationError):
            FullName("   ", "Doe")
    
    def test_empty_last_name(self):
        """Test empty last name raises ValidationError."""
        with pytest.raises(ValidationError):
            FullName("John", "")
        
        with pytest.raises(ValidationError):
            FullName("John", "   ")
    
    def test_full_name_equality(self):
        """Test full name equality comparison."""
        name1 = FullName("John", "Doe")
        name2 = FullName("John", "Doe")
        name3 = FullName("Jane", "Doe")
        
        assert name1 == name2
        assert name1 != name3


class TestHashedPassword:
    """Test cases for HashedPassword value object."""
    
    def test_valid_hashed_password(self):
        """Test creating hashed password with valid value."""
        hashed_password = HashedPassword("$2b$12$hashed_value")
        assert hashed_password.hashed_value == "$2b$12$hashed_value"
    
    def test_empty_hashed_password(self):
        """Test empty hashed password raises ValidationError."""
        with pytest.raises(ValidationError):
            HashedPassword("")
    
    def test_hashed_password_equality(self):
        """Test hashed password equality comparison."""
        password1 = HashedPassword("$2b$12$hashed_value")
        password2 = HashedPassword("$2b$12$hashed_value")
        password3 = HashedPassword("$2b$12$other_value")
        
        assert password1 == password2
        assert password1 != password3 