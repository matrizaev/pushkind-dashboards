from pushboards import db
from pushboards.auth.models import User


class UserFile(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(128), nullable=False)
    file_url = db.Column(db.String(128), nullable=False)
    file_path = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref=db.backref("files", lazy=True))

    def __init__(self, file_name: str, file_url: str, file_path: str, user: User):
        self.file_name = file_name
        self.file_url = file_url
        self.file_path = file_path
        self.user = user
