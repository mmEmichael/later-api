from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum as SAEnum
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from later_api.models.categories import Category
    from later_api.models.sources import Source


class ResourceStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"


class Resource(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    title: str | None = Field(default=None, index=True)

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
        sa_column=Column(
            SAEnum(
                ResourceStatus,
                values_callable=lambda enum: [item.value for item in enum],
            ),
            nullable=False,
            index=True,
        ),
    )

    created_at: datetime = Field(default_factory=datetime.now)

    category: Optional["Category"] = Relationship(
        back_populates="resources",
    )

    source: Optional["Source"] = Relationship(
        back_populates="resources",
    )
