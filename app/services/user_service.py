from ..models import User
from ..config import config

from sqlalchemy.orm import Session
import jsonwebtoken as jwt

ALGORITHM = 'HS256'

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def register(self, name: str, email: str, password: str, should_commit: bool = True):
        """Register a new user with hashed password."""
        # Check if the user already exists by email
        email = email.lower().strip()
        existing_user = self.session.query(User).filter(User.email == email).first()
        if existing_user:
            raise ValueError(f"User with email {email} already exists.")

        # Create new user and hash the password
        user = User(name=name, email=email)
        user.set_password(password)  # Hash the password and store it
        self.session.add(user)

        if should_commit:
            self.session.commit()

        return user
    
    def get_all_users(self):
        """Retrieve all users."""
        return self.session.query(User).all()

    def get_user(self, email: str):
        """Retrieve a user by their email."""
        # get all fields of the user
        return self.session.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int):
        """Retrieve a user by their ID."""
        return self.session.query(User).filter(User.id == user_id).first()

    def get_auth_token(self, email: str) -> str:
        """Generate an authentication token for the user."""
        jwt_payload = {'email': email}
        return jwt.encode(jwt_payload, config.SECRET_KEY, algorithm=ALGORITHM)

    def get_user_from_token(self, token: str) -> User:
        if token == "":
            return None 
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get('email')
            if email:
                return self.get_user(email)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.InvalidTokenError:
            print("Invalid token.")
        except Exception as e:
            print(f"Error decoding token: {e}")

        return None

    def login(self, email: str, password: str):
        """Login the user by verifying the password."""
        email = email.lower().strip()
        user = self.session.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            return user
        return None  # Return None if authentication fails

    def update_password(self, email: str, old_password: str, new_password: str):
        """Update the user's password after verifying the old password."""
        user = self.session.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError("User not found.")

        if not user.check_password(old_password):
            raise ValueError("Old password is incorrect.")

        user.set_password(new_password)  # Hash and update password
        self.session.commit()

        return user
