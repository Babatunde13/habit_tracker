import pytest

# Test UserService register method
def test_register(user_service, db_session):
    """Test that a new user can be registered."""
    user = user_service.register(name="New User", email="newuser@example.com", password="password123")
    
    # Check that the user is created with correct details
    assert user.name == "New User"
    assert user.email == "newuser@example.com"
    assert user.id is not None  # User should have an ID after registration


# Test UserService register with existing email
def test_register_existing_user(user_service, sample_user):
    """Test that an error is raised when trying to register with an existing email."""
    with pytest.raises(ValueError, match="User with email testuser@example.com already exists."):
        user_service.register(name="New User", email=sample_user.email, password="password123")


# Test UserService login method with correct credentials
def test_login_valid(user_service, sample_user):
    """Test that a user can log in with correct credentials."""
    user = user_service.login(sample_user.email, "pasSword@123")
    assert user is not None
    assert user.email == sample_user.email


# Test UserService login method with incorrect credentials
def test_login_invalid(user_service, sample_user):
    """Test that login fails with incorrect credentials."""
    user = user_service.login(sample_user.email, "wrongpassword")
    assert user is None


# Test UserService update_password method
def test_update_password(user_service, sample_user):
    """Test that the user's password can be updated."""
    # Update the password
    updated_user = user_service.update_password(sample_user.email, "pasSword@123", "newpassword123")
    
    # Check that the password was updated and the user can log in with the new password
    assert updated_user.check_password("newpassword123")
    
    # Try logging in with the old password (should fail)
    assert user_service.login(sample_user.email, "pasSword@123") is None
    
    # Try logging in with the new password (should succeed)
    assert user_service.login(sample_user.email, "newpassword123") is not None


# Test UserService get_auth_token method
def test_get_auth_token(user_service, sample_user):
    """Test that an authentication token can be generated."""
    token = user_service.get_auth_token(sample_user.email)
    assert token is not None  # Token should not be None
    assert isinstance(token, str)  # Token should be a string


# Test UserService get_user_from_token method
def test_get_user_from_token(user_service, sample_user):
    """Test that a user can be retrieved from an authentication token."""
    token = user_service.get_auth_token(sample_user.email)
    user_from_token = user_service.get_user_from_token(token)
    
    assert user_from_token is not None
    assert user_from_token.email == sample_user.email


# Test UserService get_user method by email
def test_get_user_by_email(user_service, sample_user):
    """Test that a user can be retrieved by their email."""
    user = user_service.get_user(sample_user.email)
    assert user is not None
    assert user.email == sample_user.email


# Test UserService get_user_by_id method
def test_get_user_by_id(user_service, sample_user):
    """Test that a user can be retrieved by their ID."""
    user = user_service.get_user_by_id(sample_user.id)
    assert user is not None
    assert user.id == sample_user.id
