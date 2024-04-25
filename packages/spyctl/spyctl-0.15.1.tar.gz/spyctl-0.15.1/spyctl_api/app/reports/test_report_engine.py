import os

import aioboto3
import pytest
from app.reports.report import Report
from app.reports.report_engine import ReportEngine
from app.reports.report_lib import ReportInput

file_bytes = b"test file contents"

API_KEY = "not_relevant_for_test"
API_URL = "not_relevant_for_test"
ORG = "test_org"


@pytest.fixture
async def mock_boto(monkeypatch):
    from moto.server import ThreadedMotoServer

    server = ThreadedMotoServer(port=0)
    server.start()
    port = server._server.socket.getsockname()[1]
    os.environ["AWS_ENDPOINT_URL"] = f"http://127.0.0.1:{port}"
    if "AWS_DEFAULT_PROFILE" in os.environ:
        del os.environ["AWS_DEFAULT_PROFILE"]
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    yield

    del os.environ["AWS_ENDPOINT_URL"]
    server.stop()


@pytest.fixture
async def bucket(mock_boto):
    bucket = "reports.mock"
    session = aioboto3.Session()
    async with session.client("s3") as s3:
        response = await s3.create_bucket(Bucket=bucket)
    yield bucket


@pytest.fixture
def engine(bucket):
    yield ReportEngine(config={"backend": {"kind": "s3", "bucket": bucket}})


@pytest.fixture
def report():
    r_input = ReportInput(
        report_id="mocktest",
        org_uid=ORG,
        report_args={
            "cluid": "clus:testcluster",
            "st": 1711020676,
            "et": 1711035028,
        },
        report_format="md",
    )

    report = Report(input=r_input)
    yield report


@pytest.mark.asyncio
async def test_generate_report(engine, report):
    try:
        await engine.generate_report(report, API_KEY, API_URL)
    except Exception:
        assert False, "register_report raised exception"


@pytest.mark.asyncio
async def test_get_report(engine, report):
    try:
        await engine.generate_report(report, API_KEY, API_URL)
    except Exception:
        assert False, "generate_report raised exception"

    try:
        retrieved = await engine.get_report(report.id, report.input.org_uid)
        assert retrieved is not None
        assert retrieved.id == report.id
        assert retrieved.input == report.input
        assert retrieved.status == report.status
        assert retrieved.change_log == report.change_log
    except Exception:
        assert False, "get_report raised exception"


@pytest.mark.asyncio
async def test_get_report_not_existing(engine):
    try:
        retrieved = await engine.get_report("not_existing", "test")
    except Exception as e:
        assert isinstance(e, KeyError)


@pytest.mark.asyncio
async def test_download_report(engine, report):
    try:
        await engine.generate_report(report, API_KEY, API_URL)
    except Exception:
        assert False, "generate_report raised exception"

    try:
        download = await engine.download_report(
            report.id, report.input.org_uid
        )
        assert os.path.exists(download)
        with open(download, "r") as f:
            result = f.read()
            for key, value in report.input.report_args.items():
                assert str(key) in result
                assert str(value) in result
    except Exception:
        assert False, "download_report raised exception"


@pytest.mark.asyncio
async def test_download_report_file_not_existing(engine):
    try:
        retrieved = await engine.download_report("not_existing", "test")
    except Exception as e:
        assert isinstance(e, KeyError)


@pytest.mark.asyncio
async def test_delete_report(engine, report):
    try:
        await engine.generate_report(report, API_KEY, API_URL)
    except Exception:
        assert False, "generate_report raised exception"

    try:
        download = await engine.download_report(
            report.id, report.input.org_uid
        )
        assert os.path.exists(download)
    except Exception:
        assert False, "download_report raised exception"

    try:
        await engine.delete_report(report.id, report.input.org_uid)
    except Exception:
        assert False, "delete_report raised exception"

    try:
        await engine.get_report(report.id, report.input.org_uid)
    except Exception as e:
        assert isinstance(e, KeyError)

    try:
        download = await engine.download_report(
            report.id, report.input.org_uid
        )
    except Exception as e:
        assert isinstance(e, KeyError)
    else:
        assert False, "download_report did not raise exception"


@pytest.mark.asyncio
async def test_list_reports(engine, report):
    try:
        for i in range(5):
            report.id = f"test_{i}"
            await engine.generate_report(report, API_KEY, API_URL)
    except Exception:
        assert False, "generate_report raised exception"

    try:
        retrieved = await engine.list_reports(report.input.org_uid)
        assert len(retrieved) >= 5
        assert all([isinstance(rep, Report) for rep in retrieved])
    except Exception:
        assert False, "list_reports raised exception"
