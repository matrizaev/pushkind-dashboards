from io import BytesIO
from pathlib import Path
from typing import Callable

import pandas as pd

from pushboards.extensions import db

ImportFn = Callable[[BytesIO], pd.DataFrame]


class UserFile(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(128), nullable=False)
    file_path = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey("reports.id"))

    report = db.relationship(
        "Report", backref=db.backref("files", lazy=True, order_by="files.columns.created_at.desc()")
    )
    user = db.relationship("User", backref=db.backref("files", lazy=True, order_by="files.columns.created_at.desc()"))

    def __init__(self, file_name: str, file_path: Path, user_id: int):
        self.file_name = file_name
        self.file_path = str(file_path)
        self.user_id = user_id

    def to_pickle(self, file_data: BytesIO, import_fn: ImportFn):
        file_df = import_fn(file_data)
        file_df.to_pickle(Path(self.file_path))

    def to_json(self) -> dict[str, str]:
        return {
            "id": self.id,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
        }

    def get_excel(self) -> BytesIO:
        # read from pickle
        result = pd.read_pickle(Path(self.file_path))

        # save to excel
        result_data = BytesIO()
        result.to_excel(result_data, index=False, header=False)
        result_data.seek(0)
        return result_data

    def get_html(self) -> str:
        # read from pickle
        result = pd.read_pickle(Path(self.file_path))

        # save to html
        return result.to_html(index=False, header=False, justify="left", classes=["table", "table-striped"])

    def remove_data(self):
        Path(self.file_path).unlink(missing_ok=True)


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    import_fn = db.Column(
        db.String(128), nullable=False, server_default="pushboards.main.upload.excel_processor.process"
    )

    def __init__(self, report_name: str, import_fn: str):
        self.report_name = report_name
        self.import_fn = import_fn

    def to_json(self) -> dict[str, str]:
        return {
            "id": self.id,
            "report_name": self.report_name,
            "created_at": self.created_at.isoformat(),
            "files": [file.to_json() for file in self.files],
        }

    def attach_import_fn(self):
        pass
