from datetime import datetime

from sqlmodel import SQLModel


class ResourceCreate(SQLModel):
    url: str
    title: str


class ResourceEdit(SQLModel):
    id: int
    url: str | None
    title: str | None
    source: str | None
    category: str | None
    status: str | None


class ResourceRead(SQLModel):
    id: int
    url: str
    title: str
    source: str
    category: str | None
    status: str
    created_at: datetime
