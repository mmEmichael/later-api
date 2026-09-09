from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class ResourceStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"


class Resource(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    title: str | None = Field(index=True)
    source: str | None = Field(default=None)
    category: str | None = Field(default=None)
    status: ResourceStatus = Field(default=ResourceStatus.UNREAD, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
