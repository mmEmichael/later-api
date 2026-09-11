from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, AnyHttpUrl
from sqlmodel import Field, SQLModel

HttpUrlString = Annotated[AnyHttpUrl, AfterValidator(str)]


class ResourceCreate(SQLModel):
    url: HttpUrlString


class ResourceEdit(SQLModel):
    id: int
    url: HttpUrlString | None = None
    title: str | None = Field(default=None, min_length=1, max_length=255)
    source_id: int | None = None
    category: str | None = None
    status: str | None = None


class ResourceRead(SQLModel):
    id: int
    url: HttpUrlString
    title: str
    source_id: int
    category: str | None
    status: str
    created_at: datetime
