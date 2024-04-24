from typing import Literal, Optional, Protocol

from pydantic import BaseModel, Field

STATUSES = Literal["scheduled", "generated", "published", "failed"]
FORMATS = Literal["md", "json", "yaml"]


class Reporter(Protocol):
    def collector(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> list: ...

    def processor(
        self,
        data: list,
        args: dict[str, str | float | int | bool],
        mock: Optional[dict] = None,
        format: Optional[str] = "md",
    ) -> dict: ...


class ReportGenerateInput(BaseModel):
    org_uid: str = Field(
        title="Organization Unique Id to generate the report for"
    )
    api_key: str = Field(
        title="API Key to access the backend data apis for the report"
    )
    api_url: str = Field(
        title="API URL to access the backend data apis for the report"
    )
    report_id: str = Field(title="Id of the report to generate")
    report_args: dict[str, str | float | int | bool] = Field(
        title="A dictionary of name/value pair arguments"
    )
    report_format: Optional[FORMATS] = Field(
        default="md", title="Format of the report to generate"
    )
    mock: dict = Field(
        title="mock json to use to aid in development of the report generation",
        default={},
    )


class ReportInput(BaseModel):
    org_uid: str = Field(
        title="Organization Unique Id to generate the report for"
    )
    report_id: str = Field(title="Id of the report to generate")
    report_args: dict[str, str | float | int | bool] = Field(
        title="A dictionary of name/value pair arguments"
    )
    report_format: Optional[FORMATS] = Field(
        default="md", title="Format of the report to generate"
    )
    mock: dict = Field(
        title="mock json to use to aid in development of the report generation",
        default={},
    )


class ReportSpecArgument(BaseModel):
    name: str = Field(title="Name of the argument")
    short: str = Field(title="Short form description of the argument")
    description: str = Field(title="Description of the argument")
    required: bool = Field(title="Is the argument required")
    type: Literal["cluster", "timestamp"] = Field(title="Type of the argument")


class ReportSpec(BaseModel):
    id: str = Field(title="Name of the report")
    short: str = Field(title="Short form description of the report")
    description: str = Field(title="Long form description of the report")
    args: list[ReportSpecArgument] = Field(
        title="List of arguments for the report"
    )


class ReportInventory(BaseModel):
    inventory: list[ReportSpec] = Field(title="List of available reports")
