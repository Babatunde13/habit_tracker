import re

def is_valid_email(email: str) -> bool:
    """
    Validate if the email is in a correct format.
    A simple regex to check if the email follows basic email format rules.
    """
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return bool(re.match(email_regex, email))

def is_number(num: int):
    return type(num) == int

def is_valid_periodicity(periodicity: str) -> bool:
    """
    Validate if the periodicity is one of the predefined values.
    """
    valid_periodicities = ['daily', 'weekly', 'fortnightly', 'monthly', 'quarterly', 'biannually', 'yearly']
    return periodicity.lower() in valid_periodicities

def is_valid_password(password: str) -> bool:
    """
    Validate the password with the following rules:
    - At least 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if len(password) < 8:
        return False

    password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;<>,.?/\\|]).{8,}$"
    return bool(re.match(password_regex, password))

def validate_register(name: str, email: str, password: str) -> bool:
    """
    Validate the inputs for user registration.
    - Name should not be empty
    - Email should be valid
    - Password should be valid
    """
    if not name:
        print("Name is required.")
        return False
    
    if not is_valid_email(email):
        print("Invalid email format.")
        return False
    
    if not is_valid_password(password):
        print("Password is invalid. Ensure it's at least 8 characters long, contains one uppercase letter, one lowercase letter, one digit, and one special character.")
        return False
    
    return True

def validate_login(email: str, password: str) -> bool:
    """
    Validate the login inputs.
    - Email should be valid
    - Password should be valid
    """
    if not is_valid_email(email):
        print("Invalid email format.")
        return False
    
    if not is_valid_password(password):
        print("Password is invalid.")
        return False
    
    return True

def validate_update_password(email: str, password: str, new_password: str) -> bool:
    """
    Validate the login inputs.
    - Email should be valid
    - Password should be valid
    """
    if not is_valid_email(email):
        print("Invalid email format.")
        return False
    
    if not is_valid_password(password):
        print("Old Password is invalid.")
        return False
    
    if not is_valid_password(new_password):
        print("New Password is invalid.")
        return False
    
    return True

def validate_create_habit(name: str, periodicity: str) -> bool:
    """
    Validate inputs for habit creation.
    - Habit name should not be empty
    - Periodicity should be one of the predefined valid values
    """
    
    # Validate habit name
    if not name:
        print("Habit name is required.")
        return False

    # Validate periodicity
    if not is_valid_periodicity(periodicity):
        print("Invalid periodicity. Valid values are: daily, weekly, fortnightly, monthly, quarterly, biannually, yearly.")
        return False
    
    return True
