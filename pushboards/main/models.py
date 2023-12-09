from io import BytesIO
from pathlib import Path
from typing import Callable

import pandas as pd

from pushboards.extensions import db

ImportFn = Callable[[BytesIO], pd.DataFrame]


class UserFile(db.Model):  # noqa: R0401, R0903
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(128), nullable=False)
    file_path = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref=db.backref("files", lazy=True))

    def __init__(
        self, file_name: str, file_path: Path, user_id: int, file_data: BytesIO, import_fn: Callable
    ):  # noqa: R0913
        self.file_name = file_name
        self.file_path = str(file_path)
        self.user_id = user_id
        file_df = import_fn(file_data)
        file_df.to_pickle(self.file_path)

    def to_json(self) -> dict[str, str]:
        return {
            "id": self.id,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "user_id": self.user_id,
        }

    def to_excel(self) -> BytesIO:
        # read from pickle
        result = pd.read_pickle(Path(self.file_path))

        # save to excel
        result_data = BytesIO()
        result.to_excel(result_data, index=False, header=False)
        result_data.seek(0)
        return result_data

    def to_html(self) -> str:
        # read from pickle
        result = pd.read_pickle(Path(self.file_path))

        # save to html
        return result.to_html(index=False, header=False, justify="left", classes=["table", "table-striped"])
