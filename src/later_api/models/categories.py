from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from later_api.models.resources import Resource


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    resources: list["Resource"] = Relationship(back_populates="category")  # noqa: UP037  # pyright: ignore[reportAny]
