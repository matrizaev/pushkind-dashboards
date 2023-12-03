from flask_login import UserMixin

from pushboards import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    full_name = db.Column(db.String(128), nullable=True)
    picture = db.Column(db.String(128), nullable=True)

    def __init__(self, email: str):
        self.email = email.lower()
