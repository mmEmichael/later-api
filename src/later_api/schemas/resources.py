from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, AnyHttpUrl
from sqlmodel import Field, SQLModel

from later_api.models.resources import ResourceStatus

HttpUrlString = Annotated[AnyHttpUrl, AfterValidator(str)]


class ResourceCreate(SQLModel):
    url: HttpUrlString


class ResourceEdit(SQLModel):
    url: HttpUrlString | None = None
    title: str | None = Field(default=None, min_length=1, max_length=255)
    source_id: int | None = None
    category_id: int | None = None
    status: ResourceStatus | None = None


class ResourceRead(SQLModel):
    id: int
    url: str
    title: str | None
    source_id: int | None
    category_id: int | None
    status: ResourceStatus
    created_at: datetime
