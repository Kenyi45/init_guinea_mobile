import pytest
from src.contexts.users.domain.services import PasswordService
from src.shared.domain.exceptions import ValidationError


class TestPasswordService:
    """Test cases for PasswordService."""
    
    def test_hash_valid_password(self):
        """Test hashing a valid password."""
        service = PasswordService()
        password = "TestPassword123"
        
        hashed = service.hash_password(password)
        
        assert hashed is not None
        assert hashed != password
        assert hashed.startswith("$2b$")
    
    def test_verify_correct_password(self):
        """Test verifying correct password."""
        service = PasswordService()
        password = "TestPassword123"
        
        hashed = service.hash_password(password)
        
        assert service.verify_password(password, hashed) is True
    
    def test_verify_incorrect_password(self):
        """Test verifying incorrect password."""
        service = PasswordService()
        password = "TestPassword123"
        wrong_password = "WrongPassword123"
        
        hashed = service.hash_password(password)
        
        assert service.verify_password(wrong_password, hashed) is False
    
    def test_hash_password_too_short(self):
        """Test hashing password that's too short raises ValidationError."""
        service = PasswordService()
        
        with pytest.raises(ValidationError):
            service.hash_password("short")
    
    def test_hash_password_no_uppercase(self):
        """Test hashing password without uppercase raises ValidationError."""
        service = PasswordService()
        
        with pytest.raises(ValidationError):
            service.hash_password("testpassword123")
    
    def test_hash_password_no_lowercase(self):
        """Test hashing password without lowercase raises ValidationError."""
        service = PasswordService()
        
        with pytest.raises(ValidationError):
            service.hash_password("TESTPASSWORD123")
    
    def test_hash_password_no_digit(self):
        """Test hashing password without digit raises ValidationError."""
        service = PasswordService()
        
        with pytest.raises(ValidationError):
            service.hash_password("TestPassword")
    
    def test_hash_empty_password(self):
        """Test hashing empty password raises ValidationError."""
        service = PasswordService()
        
        with pytest.raises(ValidationError):
            service.hash_password("")
    
    def test_password_validation_requirements(self):
        """Test various password validation scenarios."""
        service = PasswordService()
        
        # Valid passwords
        valid_passwords = [
            "TestPassword123",
            "MySecurePassword1",
            "ValidPass123",
            "StrongPassword2024"
        ]
        
        for password in valid_passwords:
            try:
                service.hash_password(password)
            except ValidationError:
                pytest.fail(f"Password '{password}' should be valid")
        
        # Invalid passwords
        invalid_passwords = [
            "short",                    # Too short
            "testpassword123",         # No uppercase
            "TESTPASSWORD123",         # No lowercase
            "TestPassword",            # No digit
            "",                        # Empty
            "NoDigits"                 # No digits
        ]
        
        for password in invalid_passwords:
            with pytest.raises(ValidationError):
                service.hash_password(password) 