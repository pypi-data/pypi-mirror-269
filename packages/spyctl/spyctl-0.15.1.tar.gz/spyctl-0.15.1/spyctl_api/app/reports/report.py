from __future__ import annotations

import time
import uuid
from typing import Optional, Tuple

import app.reports.report_lib as rlib
from pydantic import BaseModel, Field


class Report(BaseModel):
    id: Optional[str] = Field(None, title="Id of the report")
    input: rlib.ReportInput = Field(title="Input for the report")
    status: rlib.STATUSES = Field(
        title="Status of the report generation", default="scheduled"
    )
    error: Optional[str] = Field(
        title="Error message if the report failed", default=None
    )
    change_log: list[Tuple[float, dict]] = Field(
        title="Log of changes to the report", default=[]
    )

    def __init__(self, **kw):
        super().__init__(**kw)
        if "id" not in kw:
            self.id = uuid.uuid4().hex

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.change_log.append((time.time(), kwargs))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "input": self.input.dict(),
            "status": self.status,
            "error": self.error,
            "change_log": self.change_log,
        }

    @staticmethod
    def from_dict(data: dict) -> Report:
        report = Report.parse_obj(data)
        report.id = data["id"]
        return report
