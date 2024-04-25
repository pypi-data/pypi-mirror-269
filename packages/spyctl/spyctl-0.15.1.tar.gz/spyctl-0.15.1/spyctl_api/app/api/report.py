from __future__ import annotations

from typing import Annotated

import app.reports.report_engine as report_engine
import app.reports.report_lib as rlib
from app.reports.report import Report
from app.reports.report_engine import ReportEngine, make_engine
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
import app.config


router = APIRouter(prefix="/api/v1")


def get_engine():
    return make_engine(
        {
            "backend": {
                "kind": app.config.get("report_backend_kind", fallback="s3"),
                "aws_access_key_id": app.config.get("aws_access_key_id"),
                "aws_secret_access_key": app.config.get(
                    "aws_secret_access_key"
                ),
                "aws_role_arn": app.config.get("aws_role_arn"),
                "bucket": app.config.get("report_bucket", fallback="reports"),
            }
        }
    )


EngineDep = Annotated[ReportEngine, Depends(get_engine)]


# ------------------------------------------------------------------------------
# Report Service
# ------------------------------------------------------------------------------


@router.get("/report/inventory")
def inventory(engine: EngineDep) -> rlib.ReportInventory:
    inv = engine.get_inventory()
    return rlib.ReportInventory.parse_obj(inv)


@router.post("/report/generate")
def generate(
    i: rlib.ReportGenerateInput,
    background_tasks: BackgroundTasks,
    engine: EngineDep,
) -> Report:

    core_input = rlib.ReportInput(
        org_uid=i.org_uid,
        report_id=i.report_id,
        report_args=i.report_args,
        report_format=i.report_format,
    )
    report = Report(input=core_input)
    background_tasks.add_task(
        engine.generate_report, report, i.api_key, i.api_url
    )
    return report


@router.get("/report/status")
async def get_report_status(
    id: str, org_uid: str, engine: EngineDep
) -> Report:
    try:
        report = await engine.get_report(id, org_uid)
        return report
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Report {id} for org {org_uid} not found"
        )


@router.get("/report/download")
async def download_report(id: str, org_uid: str, engine: EngineDep):

    try:
        engine = report_engine.get_engine()
        report = await engine.get_report(id, org_uid)
        if report.status != "published":
            raise HTTPException(status_code=404, detail="Report not published")

        download = await engine.download_report(id, org_uid)
        return FileResponse(
            path=download,
            filename=f"{report.input.report_id}.{report.input.report_format}",
        )

    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Report {id} for org {org_uid} not found"
        )


@router.delete("/report")
async def delete_report(id: str, org_uid: str, engine: EngineDep):

    try:
        await engine.delete_report(id, org_uid)
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Report {id} for org {org_uid} not found"
        )


@router.get("/report/list")
async def list_reports(org_uid: str, engine: EngineDep) -> list[Report]:

    try:
        reports = await engine.list_reports(org_uid)
        return reports
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"No reports found for org {org_uid}"
        )
