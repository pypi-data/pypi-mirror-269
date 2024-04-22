from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field, conint, constr

from iap_cli.models.enums import Method, State


class Query(BaseModel):
    endpoint: str
    method: Optional[Method] = Field("get", description="HTTP method")
    data: dict = None
    jsonbody: dict = None
    params: dict = None


class AdaptersHealthResult(BaseModel):
    id: Optional[str] = Field(None, examples=["ServiceNow"])
    package_id: Optional[constr(pattern=r"^@[-_.a-z]+/.+")] = Field(
        "",
        description="The model used by the service",
        examples=["@itential/adapter-local_aaa"],
        title="Model",
    )
    type: Optional[str] = None
    description: Optional[str] = Field(None, examples=["A basic description"])
    state: Optional[State] = None
    connection: Optional[dict[str, Any]] = None
    routePrefix: Optional[str] = Field(None, examples=["admin", "search"])

    class Config:
        use_enum_values = True


class AdaptersHealthGetResponse(BaseModel):
    results: Optional[list[AdaptersHealthResult]] = None
    total: Optional[conint(ge=0)] = Field(
        None, description="The total number of adapters", examples=[1, 5, 10, 20, 50]
    )


class ApplicationsHealthResult(BaseModel):
    id: Optional[str] = Field(None, examples=["AdminEssentials"])
    package_id: Optional[constr(pattern=r"^@[-_.a-z]+/.+")] = Field(
        "",
        description="The model used by the service",
        examples=["@itential/app-workflow_engine"],
        title="Model",
    )
    type: Optional[str] = None
    description: Optional[str] = Field(None, examples=["A basic description"])
    state: Optional[State] = None
    connection: Optional[dict[str, Any]] = None
    routePrefix: Optional[str] = Field(None, examples=["admin", "search"])

    class Config:
        use_enum_values = True


class ApplicationsHealthGetResponse(BaseModel):
    results: Optional[list[ApplicationsHealthResult]] = None
    total: Optional[conint(ge=0)] = Field(
        None,
        description="The total number of applications",
        examples=[1, 5, 10, 20, 50],
    )
