import os
import uuid

import aioboto3
import pytest
from app.reports.report_engine import ReportEngine
from fastapi.testclient import TestClient
from moto.server import ThreadedMotoServer

from .main import app


@pytest.fixture
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
    os.environ["REPORT_BUCKET"] = bucket
    yield bucket


@pytest.fixture
def engine(bucket):
    yield ReportEngine(config={"backend": {"kind": "s3", "bucket": bucket}})


@pytest.fixture
def client(engine):
    yield TestClient(app)


@pytest.fixture
def reportid(client):
    response = client.post("/api/v1/report/generate", json=report_input)
    id = response.json()["id"]
    yield id


API_KEY = os.environ.get("INTEGRATION_API_KEY", "test")
API_URL = os.environ.get("API_URL", "https://api.kangaroobat.net")
ORG = os.environ.get("ORG", "KNUJF8M43WcT2o1qgEts")
CLUSTER = os.environ.get("CLUSTER", "clus:VyTE0-BPVmo")
report_input = {
    "report_id": "mocktest",
    "org_uid": ORG,
    "api_key": API_KEY,
    "api_url": API_URL,
    "report_args": {"cluid": CLUSTER, "st": 1711020676, "et": 1711035028},
}


def test_get_inventory(client):
    response = client.get("/api/v1/report/inventory")
    assert response.status_code == 200
    result = response.json()
    assert "inventory" in result
    assert len(result["inventory"]) > 0


def test_generate_report(client):
    response = client.post("/api/v1/report/generate", json=report_input)
    if response.status_code != 200:
        print(f"input was: ", report_input)
        print(f"api response text: ", response.text)
    assert response.status_code == 200
    result = response.json()

    assert result["id"] != ""


def test_status_report_existing(client, reportid):
    data = {"org_uid": ORG, "id": reportid}
    response = client.get(f"/api/v1/report/status", params=data)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == reportid
    assert result["status"] == "published"


def test_status_report_not_existing(client):
    data = {"org_uid": ORG, "id": "not_existing"}
    response = client.get("/api/v1/report/status", params=data)
    assert response.status_code == 404


def test_download_report_existing(client, reportid):
    data = {"org_uid": ORG, "id": reportid}
    response = client.get("/api/v1/report/download", params=data)
    assert response.status_code == 200
    result = response.text
    for key, value in report_input["report_args"].items():
        assert str(key) in result
        assert str(value) in result
    assert len(result) > 0


def test_download_report_not_existing(client):
    data = {"org_uid": ORG, "id": "not_existing"}
    response = client.get("/api/v1/report/download", params=data)
    assert response.status_code == 404


def test_delete_report_existing(client, reportid):
    data = {"org_uid": ORG, "id": reportid}
    response = client.delete("/api/v1/report", params=data)
    assert response.status_code == 200

    data = {"org_uid": ORG, "id": reportid}
    response = client.get("/api/v1/report/status", params=data)
    assert response.status_code == 404


def test_list_reports(client):
    for i in range(5):
        response = client.post("/api/v1/report/generate", json=report_input)

    data = {"org_uid": ORG}
    response = client.get("/api/v1/report/list", params=data)
    assert response.status_code == 200
    result = response.json()
    assert len(result) >= 5
    assert "id" in result[0]
    assert "status" in result[0]
    assert "input" in result[0]
