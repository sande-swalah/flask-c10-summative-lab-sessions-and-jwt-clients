from sqlalchemy.orm import validates

from app.config import bcrypt, db
from app.validator.user_validator import validate_username_value


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password_hash = db.Column("password_hash", db.String(255))

    journal_entries = db.relationship(
        "JournalEntry",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed")

    @password_hash.setter
    def password_hash(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
        }
