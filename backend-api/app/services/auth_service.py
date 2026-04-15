from sqlalchemy.exc import IntegrityError

from app.errors import UnauthorizedError, ValidationError
from app.repositories.user_repository import UserRepository
from app.validator.authenticator import SessionAuthenticator
from models import User


class AuthService:
    def __init__(self, user_repository=None, authenticator=None):
        self.user_repository = user_repository or UserRepository()
        self.authenticator = authenticator or SessionAuthenticator(self.user_repository)

    def signup(self, payload):
        username = payload["username"].strip()
        password = payload["password"]

        try:
            user = User(username=username)
            user.password_hash = password
            self.user_repository.add(user)
            self.user_repository.commit()
        except ValueError as err:
            self.user_repository.rollback()
            raise ValidationError(str(err))
        except IntegrityError:
            self.user_repository.rollback()
            raise ValidationError("Username already exists")

        self.authenticator.login(user.id)
        return user

    def login(self, payload):
        username = payload["username"].strip()
        password = payload["password"]

        user = self.user_repository.get_by_username(username)
        if not user or not user.authenticate(password):
            raise UnauthorizedError("Invalid username or password")

        self.authenticator.login(user.id)
        return user

    def check_session(self):
        return self.authenticator.require_user()

    def logout(self):
        self.authenticator.logout()
