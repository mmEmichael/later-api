from datetime import datetime

from sqlmodel import Field, SQLModel


class Resource(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    title: str = Field(index=True)
    source: str | None = Field(default=None)
    category: str | None = Field(default=None)
    status: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
