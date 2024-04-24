from __future__ import annotations
from datetime import datetime, timedelta
import asyncio
import json
from typing import Tuple

import aioboto3
from app.reports.report_engine import Report
from botocore.exceptions import ClientError


def id_2_meta_key(id: str, org_uid: str) -> str:
    return f"reports/{org_uid}/meta/{id}.json"


def id_2_file_key(id: str, org_uid: str) -> str:
    return f"reports/{org_uid}/files/{id}.report"


def org_2_prefix(org_uid: str) -> str:
    return f"reports/{org_uid}/meta/"


class S3Backend:
    def __init__(self, backend_config: dict):
        self.bucket = backend_config["bucket"]
        self.aws_access_key_id = backend_config.get("aws_access_key_id")
        self.aws_secret_access_key = backend_config.get(
            "aws_secret_access_key"
        )
        self.aws_secret_access_key = backend_config.get(
            "aws_secret_access_key"
        )
        self.aws_role_arn = backend_config.get("aws_role_arn")
        self.session = None
        self.assumed_role = None

    async def ensure_session(self):
        # if we already have a session, we just need to check if we are
        # using an assumed role and it's creds aren't expired yet.
        if self.session:
            if not self.aws_role_arn:
                return
            if self.assumed_role:
                expiration = self.assumed_role["Credentials"]["Expiration"]
                if datetime.now(expiration.tzinfo) < expiration - timedelta(
                    minutes=5
                ):
                    return

        if self.aws_access_key_id and self.aws_secret_access_key:
            self.session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            )

            if self.aws_role_arn:
                async with self.session.client("sts") as sts_client:
                    self.assumed_role = await sts_client.assume_role(
                        RoleArn=self.aws_role_arn, RoleSessionName="gd"
                    )
                    creds = self.assumed_role["Credentials"]
                    self.session = aioboto3.Session(
                        aws_access_key_id=creds["AccessKeyId"],
                        aws_secret_access_key=creds["SecretAccessKey"],
                        aws_session_token=creds["SessionToken"],
                    )
            return

        self.session = aioboto3.Session()

    async def register_report(self, report: Report):
        await self.ensure_session()
        async with self.session.client("s3") as s3:
            try:
                await s3.put_object(
                    Bucket=self.bucket,
                    Key=id_2_meta_key(report.id, report.input.org_uid),
                    Body=json.dumps(report.to_dict()),
                )
            except Exception as e:
                raise self.handle_error(e)

    async def update_report(self, report: Report):
        await self.register_report(report)

    async def get_report(self, id: str, org_uid: str) -> Report:
        await self.ensure_session()
        async with self.session.client("s3") as s3:
            try:
                response = await s3.get_object(
                    Bucket=self.bucket, Key=id_2_meta_key(id, org_uid)
                )
                data = await response["Body"].read()
                report = Report.from_dict(json.loads(data))
                return report
            except Exception as e:
                raise self.handle_error(e)

    async def delete_report(self, id: str, org_uid: str):
        await self.ensure_session()
        async with self.session.client("s3") as s3:
            try:
                await asyncio.gather(
                    s3.delete_object(
                        Bucket=self.bucket, Key=id_2_meta_key(id, org_uid)
                    ),
                    s3.delete_object(
                        Bucket=self.bucket, Key=id_2_file_key(id, org_uid)
                    ),
                )
            except Exception as e:
                raise self.handle_error(e)

    async def list_reports(self, org_uid: str):
        rv = []
        await self.ensure_session()
        async with self.session.client("s3") as s3:
            # List all files under the common key
            response = await s3.list_objects_v2(
                Bucket=self.bucket, Prefix=org_2_prefix(org_uid)
            )
            for item in response.get("Contents", []):
                file_key = item["Key"]
                # Download each file
                response = await s3.get_object(
                    Bucket=self.bucket, Key=file_key
                )
                data = await response["Body"].read()
                rv.append(Report.from_dict(json.loads(data)))
        return rv

    async def publish_report_file(
        self, report: Report, report_bytes: bytes
    ) -> None:

        await self.ensure_session()
        async with self.session.client("s3") as s3:
            try:
                await s3.put_object(
                    Bucket=self.bucket,
                    Key=id_2_file_key(report.id, report.input.org_uid),
                    Body=report_bytes,
                )
            except Exception as e:
                raise self.handle_error(e)

    async def download_report_file(self, id: str, org_uid: str) -> str:
        await self.ensure_session()
        async with self.session.client("s3") as s3:
            try:
                key = id_2_file_key(id, org_uid)
                filename = f"/tmp/{id}"
                await s3.download_file(self.bucket, key, filename)
                return filename
            except Exception as e:
                raise self.handle_error(e)

    def handle_error(self, e: Exception) -> Exception:
        if isinstance(e, ClientError):
            if e.response["Error"]["Code"] in ["NoSuchKey", "404"]:
                return KeyError(f"Report not found")
            elif e.response["Error"]["Code"] == "AccessDenied":
                return PermissionError(f"Access denied")
            elif e.response["Error"]["Code"] == "BucketNotFound":
                return ValueError(f"s3 backend bucket not found")
            else:
                return ValueError(f"s3 backend error: {e}")
        else:
            return e
