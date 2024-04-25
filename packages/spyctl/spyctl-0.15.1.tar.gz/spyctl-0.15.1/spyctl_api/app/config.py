from __future__ import annotations

import json
import os
from typing import Any, Optional

import aioboto3

_config = dict()


def deployment_2_bucket(deployment: str) -> str:
    # TODO
    # externalize special cases to config file
    # or env vars
    if deployment == "staging":
        return "staging.tigerbat.deployments"
    return f"{deployment}.spyderbat.deployments"


async def make_session():
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_role_arn = os.getenv("AWS_ROLE_ARN")
    if aws_access_key_id and aws_secret_access_key:
        session = aioboto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        if aws_role_arn:
            async with session.client("sts") as sts_client:
                assumed_role = await sts_client.assume_role(
                    RoleArn=aws_role_arn, RoleSessionName="gd"
                )
                creds = assumed_role["Credentials"]
                session = aioboto3.Session(
                    aws_access_key_id=creds["AccessKeyId"],
                    aws_secret_access_key=creds["SecretAccessKey"],
                    aws_session_token=creds["SessionToken"],
                )
        return session

    session = aioboto3.Session()
    return session


async def load_config():
    global _config
    print("Spyctl API config loading...")
    _config = {}
    deployment = os.getenv("DEPLOYMENT")
    if not deployment:
        raise Exception("DEPLOYMENT env var not set")
    print("Spyctl API config - DEPLOYMENT is:", deployment)
    config_bucket = deployment_2_bucket(deployment)
    config_key = f"builds/1/ec2/spyctl/spyctl-{deployment}.config"
    try:
        config_file = await load_s3_config(config_bucket, config_key)
        _config = json.loads(config_file)
        print(
            "Spyctl API config loaded successfully from "
            f"s3://{config_bucket}/{config_key}"
        )
    except Exception as e:
        print(
            f"Spyctl API config failed to load from s3://{config_bucket}/{config_key}: {e}.\n"
            "Spyctl API config Falling back to env vars"
        )
        return


async def load_s3_config(bucket, key):
    # load file from s3 bucket and key with aioboto3
    session = await make_session()
    async with session.client("s3") as s3:
        response = await s3.get_object(Bucket=bucket, Key=key)
        file_content = await response["Body"].read()
        return file_content


def get(arg: str, fallback: Optional[Any] = None):
    return _config.get(arg, os.getenv(arg.upper(), fallback))
