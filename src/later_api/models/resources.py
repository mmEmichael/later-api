from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from later_api.models.categories import Category
    from later_api.models.sources import Source


class ResourceStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"


class Resource(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    title: str | None = Field(index=True)
    source_id: int | None = Field(
        default=None,
        foreign_key="source.id",
    )
    category_id: int | None = Field(
        default=None,
        foreign_key="category.id",
    )
    status: ResourceStatus = Field(
        default=ResourceStatus.UNREAD,
        index=True,
    )
    created_at: datetime = Field(default_factory=datetime.now)

    category: "Category | None" = Relationship(back_populates="resources")  # noqa: UP037  # pyright: ignore[reportAny]
    source: "Source | None" = Relationship(back_populates="resources")  # noqa: UP037  # pyright: ignore[reportAny]
