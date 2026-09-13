from sqlmodel import Field, SQLModel


class CategoryCreate(SQLModel):
    name: str = Field(min_length=1, max_length=255)


class CategoryEdit(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)


class CategoryRead(SQLModel):
    id: int
    name: str
