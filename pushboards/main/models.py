from pathlib import Path
from uuid import uuid4

from flask import current_app, url_for
from werkzeug.datastructures import FileStorage

from pushboards.extensions import db


class UserFile(db.Model):  # noqa: R0401, R0903
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(128), nullable=False)
    file_url = db.Column(db.String(128), nullable=False)
    file_path = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref=db.backref("files", lazy=True))

    def __init__(self, file_post: FileStorage, user_id: int, process_fn: callable):
        file_path = Path(current_app.config["STATIC_UPLOAD_PATH"])
        file_path = file_path / uuid4().hex
        file_path = file_path.with_suffix(current_app.config["FILE_UPLOAD_SUFFIX"])
        file_path = Path(current_app.static_folder) / file_path

        file_data = process_fn(file_post.stream)
        file_path.write_bytes(file_data)

        self.file_path = str(file_path)
        self.file_name = file_post.filename
        self.user_id = user_id
        self.file_url = url_for("static", filename=file_path.relative_to(current_app.static_folder))

    def to_json(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "file_url": self.file_url,
            "file_path": self.file_path,
            "user_id": self.user_id,
        }
