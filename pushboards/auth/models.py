from flask_login import UserMixin

from pushboards.extensions import db


class User(db.Model, UserMixin):  # noqa: R0903
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    full_name = db.Column(db.String(128), nullable=True)
    picture = db.Column(db.String(128), nullable=True)

    def __init__(self, email: str):
        self.email = email.lower()

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "picture": self.picture,
            "files": [file.to_json() for file in self.files],
        }
