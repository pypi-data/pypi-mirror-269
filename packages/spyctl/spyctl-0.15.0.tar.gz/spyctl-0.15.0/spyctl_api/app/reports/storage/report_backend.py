from typing import Protocol

from app.reports.report import Report
from app.reports.report_lib import ReportInput

# TODO add a background task to regularly save tasks


class ReportBackend(Protocol):

    async def register_report(self, report: Report): ...

    async def update_report(self, report: Report): ...

    async def get_report(self, id: str, org_uid: str) -> Report: ...

    async def delete_report(self, id: str, org_uid: str): ...

    async def list_reports(self, org_uid: str) -> list[Report]: ...

    async def publish_report_file(
        self, report: Report, report_bytes: bytes
    ): ...

    async def download_report_file(self, id, org_uid: str) -> str: ...


def get_backend(backend_config: dict) -> ReportBackend:
    if backend_config["kind"] == "s3":
        from app.reports.storage.s3_backend import S3Backend

        backend = S3Backend(backend_config)
        return backend
    else:
        raise ValueError("Unsupported backend kind")
