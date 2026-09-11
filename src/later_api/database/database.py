from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

import later_api.models  # noqa: F401 — регистрирует все мапперы  # pyright: ignore[reportUnusedImport]
from later_api.config import settings

engine = create_engine(settings.DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
