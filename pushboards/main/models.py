from pushboards.auth.models import User
from pushboards.extensions import db


class UserFile(db.Model):  # noqa: R0401, R0903
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

    def to_json(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "file_url": self.file_url,
            "file_path": self.file_path,
            "user_id": self.user_id,
        }

    def process(self):
        pass
