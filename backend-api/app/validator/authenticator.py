from flask import session


from app.repositories.user_repository import UserRepository


class SessionAuthenticator:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def get_current_user(self):
        user_id = session.get("user_id")
        if not user_id:
            return None
        return self.user_repository.get_by_id(user_id)

    def require_user(self):
        user = self.get_current_user()

    def login(self, user_id):
        session["user_id"] = user_id

    def logout(self):
        session.pop("user_id", None)
