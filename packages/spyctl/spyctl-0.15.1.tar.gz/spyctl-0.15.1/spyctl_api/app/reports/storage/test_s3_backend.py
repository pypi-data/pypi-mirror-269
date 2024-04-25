import os

import aioboto3
import pytest
from app.reports.report import Report
from app.reports.report_engine import ReportEngine
from app.reports.report_lib import ReportInput
from moto.server import ThreadedMotoServer

file_bytes = b"test file contents"


@pytest.fixture()
async def mock_boto(monkeypatch):
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
def s3_backend(engine):
    yield engine.backend


@pytest.fixture
def report():
    r_input = ReportInput(
        org_uid="test",
        report_id="test",
        report_args={"test": "test"},
        report_format="md",
    )
    report = Report(input=r_input)
    yield report


@pytest.mark.asyncio
async def test_register_report(s3_backend, report):
    try:
        await s3_backend.register_report(report)
        print(f"test register_report - {report.id}")
    except Exception:
        assert False, f"register_report {report.it} raised exception"


@pytest.mark.asyncio
async def test_get_report(s3_backend, report):
    try:
        await s3_backend.register_report(report)
    except Exception:
        assert False, "register_report raised exception"
    try:
        retrieved = await s3_backend.get_report(
            report.id, report.input.org_uid
        )
        assert retrieved is not None
        assert retrieved.id == report.id
        assert retrieved.input == report.input
        assert retrieved.status == report.status
        assert retrieved.change_log == report.change_log
    except Exception:
        assert False, "get_report raised exception"


@pytest.mark.asyncio
async def test_get_report_not_existing(s3_backend):
    try:
        retrieved = await s3_backend.get_report("not_existing", "test")
    except Exception as e:
        assert isinstance(e, KeyError)
    else:
        assert False, "get_report did not raise exception"


@pytest.mark.asyncio
async def test_update_report(s3_backend, report):
    report.status = "published"
    try:
        await s3_backend.update_report(report)
    except Exception:
        assert False, "update_report raised exception"
    try:
        retrieved = await s3_backend.get_report(
            report.id, report.input.org_uid
        )
        assert retrieved is not None
        assert retrieved.id == report.id
        assert retrieved.input == report.input
        assert retrieved.status == report.status
        assert retrieved.change_log == report.change_log
    except Exception:
        assert False, "get_report raised exception"


@pytest.mark.asyncio
async def test_publish_report_file(s3_backend, report):
    try:
        await s3_backend.publish_report_file(report, file_bytes)
    except Exception:
        assert False, "publish_report_file raised exception"


@pytest.mark.asyncio
async def test_download_report_file(s3_backend, report):
    try:
        await s3_backend.publish_report_file(report, file_bytes)
    except Exception:
        assert False, "publish_report_file raised exception"

    try:
        download = await s3_backend.download_report_file(
            report.id, report.input.org_uid
        )
        assert os.path.exists(download)
        with open(download, "rb") as f:
            assert f.read() == file_bytes
    except Exception:
        assert False, "publish_report_file raised exception"


@pytest.mark.asyncio
async def test_download_report_file_not_existing(s3_backend):
    try:
        retrieved = await s3_backend.download_report_file(
            "not_existing", "test"
        )
    except Exception as e:
        assert isinstance(e, KeyError)
    else:
        assert False, "download_report_file did not raise exception"


@pytest.mark.asyncio
async def test_delete_report(s3_backend, report):
    try:
        await s3_backend.register_report(report)
    except Exception:
        assert False, "register_report raised exception"

    try:
        await s3_backend.publish_report_file(report, file_bytes)
    except Exception:
        assert False, "publish_report_file raised exception"

    try:
        await s3_backend.delete_report(report.id, report.input.org_uid)
    except Exception:
        assert False, "delete_report raised exception"

    try:
        report = await s3_backend.get_report(report.id, report.input.org_uid)
    except Exception as e:
        assert isinstance(e, KeyError)
    else:
        assert False, "get_report did not raise exception"


@pytest.mark.asyncio
async def test_list_reports(s3_backend, report):
    try:
        for i in range(5):
            report.id = f"test_{i}"
            await s3_backend.register_report(report)
        retrieved = await s3_backend.list_reports("test")
        assert len(retrieved) >= 5
        assert isinstance(retrieved[0], Report)
    except Exception:
        assert False, "list_reports raised exception"
