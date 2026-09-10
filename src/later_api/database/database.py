from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from later_api.config import settings
from later_api.models.categories import (
    Category,  # pyright: ignore[reportUnusedImport] # noqa: F401
)
from later_api.models.resources import (
    Resource,  # pyright: ignore[reportUnusedImport]  # noqa: F401
)
from later_api.models.sources import (
    Source,  # pyright: ignore[reportUnusedImport]  # noqa: F401
)

engine = create_engine(settings.DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
