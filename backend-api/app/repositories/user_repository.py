from app.config import db
from models import User


class UserRepository:
    def get_by_id(self, user_id):
        return db.session.get(User, user_id)

    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def add(self, user):
        db.session.add(user)

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()
