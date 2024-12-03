import pytest
from validation import (
    is_valid_email, 
    is_number, 
    is_valid_periodicity, 
    is_valid_password, 
    validate_register,
    validate_login,
    validate_update_password,
    validate_create_habit
)

# Tests for is_valid_email function
def test_valid_email():
    assert is_valid_email("test@example.com") == True

def test_invalid_email():
    assert is_valid_email("test@example") == False
    assert is_valid_email("test.com") == False
    assert is_valid_email("test@.com") == False


# Tests for is_number function
def test_is_number():
    assert is_number(5) == True
    assert is_number("5") == False
    assert is_number(5.0) == False
    assert is_number(None) == False


# Tests for is_valid_periodicity function
def test_valid_periodicity():
    assert is_valid_periodicity("daily") == True
    assert is_valid_periodicity("weekly") == True
    assert is_valid_periodicity("monthly") == True
    assert is_valid_periodicity("yearly") == True

def test_invalid_periodicity():
    assert is_valid_periodicity("hourly") == False
    assert is_valid_periodicity("bi-weekly") == False
    assert is_valid_periodicity("fortnightly") == True  # Valid periodicity (typo fixed)


# Tests for is_valid_password function
def test_valid_password():
    valid_passwords = [
        "Password123!",
        "MySecure123@",
        "Password@1234"
    ]
    for password in valid_passwords:
        assert is_valid_password(password) == True

def test_invalid_password():
    invalid_passwords = [
        "short",  # Too short
        "password123",  # Missing uppercase and special character
        "PASSWORD123!",  # Missing lowercase
        "Password!",  # Missing digit
    ]
    for password in invalid_passwords:
        assert is_valid_password(password) == False


# Tests for validate_register function
def test_validate_register_valid():
    assert validate_register("John Doe", "john@example.com", "Password123!") == True

def test_validate_register_invalid_name():
    assert validate_register("", "john@example.com", "Password123!") == False

def test_validate_register_invalid_email():
    assert validate_register("John Doe", "john@example", "Password123!") == False

def test_validate_register_invalid_password():
    assert validate_register("John Doe", "john@example.com", "short") == False


# Tests for validate_login function
def test_validate_login_valid():
    assert validate_login("john@example.com", "Password123!") == True

def test_validate_login_invalid_email():
    assert validate_login("john@example", "Password123!") == False

def test_validate_login_invalid_password():
    assert validate_login("john@example.com", "short") == False


# Tests for validate_update_password function
def test_validate_update_password_valid():
    assert validate_update_password("john@example.com", "Password123!", "NewPassword@123") == True

def test_validate_update_password_invalid_email():
    assert validate_update_password("john@example", "Password123!", "NewPassword@123") == False

def test_validate_update_password_invalid_password():
    assert validate_update_password("john@example.com", "short", "NewPassword@123") == False

def test_validate_update_password_invalid_new_password():
    assert validate_update_password("john@example.com", "Password123!", "short") == False


# Tests for validate_create_habit function
def test_validate_create_habit_valid():
    assert validate_create_habit("Exercise", "daily") == True
    assert validate_create_habit("Study", "weekly") == True

def test_validate_create_habit_invalid_name():
    assert validate_create_habit("", "daily") == False

def test_validate_create_habit_invalid_periodicity():
    assert validate_create_habit("Exercise", "hourly") == False
    assert validate_create_habit("Exercise", "bi-weekly") == False
