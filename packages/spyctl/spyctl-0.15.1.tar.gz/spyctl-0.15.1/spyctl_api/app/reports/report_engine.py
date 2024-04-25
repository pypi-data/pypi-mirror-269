from __future__ import annotations

import importlib
import pkgutil
from typing import Optional

import app.reports.report_lib as rlib
import app.reports.storage.report_backend as report_backend
import yaml
from app.reports.report import Report
from jinja2 import Environment, PackageLoader

_engine: Optional[ReportEngine] = None


class ReportEngine:
    def __init__(self, config: dict):
        backend_config = config["backend"]
        self.backend: report_backend.ReportBackend = (
            report_backend.get_backend(backend_config)
        )
        data = pkgutil.get_data("app", "reports/portfolio/inventory.yaml")
        self.inventory: dict = yaml.safe_load(data)

    def get_inventory(self) -> dict:
        return self.inventory

    async def generate_report(
        self, report: Report, api_key: str, api_url: str
    ):
        try:
            await self.backend.register_report(report)
            gen_report = self.make_report(
                i=report.input, api_key=api_key, api_url=api_url
            )
            await self.backend.publish_report_file(
                report, report_bytes=gen_report.encode("utf-8")
            )
            report.update(status="published")
            await self.backend.update_report(report)

        except Exception as e:
            report.update(status="failed", error=repr(e))
            await self.backend.update_report(report)
            raise e

    async def download_report(self, id: str, org_uid: str) -> str:
        return await self.backend.download_report_file(id, org_uid)

    async def get_report(self, id: str, org_uid: str) -> Report:
        return await self.backend.get_report(id, org_uid)

    async def delete_report(self, id: str, org_uid: str):
        await self.backend.delete_report(id, org_uid)

    async def list_reports(self, org_uid: str) -> list[Report]:
        return await self.backend.list_reports(org_uid)

    def get_report_spec(self, report: str):
        reports = self.get_inventory()["inventory"]
        spec = [r for r in reports if r["id"] == report]
        if not spec:
            raise ValueError(f"Report {report} not found")
        return spec[0]

    def get_template(self, report: str, format: rlib.FORMATS):
        environment = Environment(
            loader=PackageLoader("app.reports.portfolio", "templates")
        )
        spec = self.get_report_spec(report)
        template = spec["templates"][format]
        return environment.get_template(template)

    def get_reporter(self, report: str) -> rlib.Reporter:
        spec = self.get_report_spec(report)
        reporter_str = spec["reporter"]
        mod_str, cls_str = reporter_str.rsplit(".", 1)
        mod = importlib.import_module(mod_str)
        cls = getattr(mod, cls_str)
        return cls()

    def make_report(
        self, i: rlib.ReportInput, api_key: str, api_url: str
    ) -> str:
        reporter = self.get_reporter(i.report_id)
        template = self.get_template(i.report_id, i.report_format)
        data = reporter.collector(
            args=i.report_args,
            org_uid=i.org_uid,
            api_key=api_key,
            api_url=api_url,
        )
        context = reporter.processor(
            data=data, args=i.report_args, format=i.report_format
        )
        report = template.render(context)
        return report


def make_engine(config: dict) -> ReportEngine:
    global _engine
    if not _engine:
        _engine = ReportEngine(config)
    return _engine


def get_engine() -> ReportEngine:
    global _engine
    if not _engine:
        raise ValueError("Report engine not initialized")
    return _engine
