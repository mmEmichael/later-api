from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

import later_api.models  # noqa: F401 — регистрирует все мапперы  # pyright: ignore[reportUnusedImport]
from later_api.config import settings

engine = create_engine(settings.DATABASE_URL)


def create_db_and_tables() -> None:
    """Create tables from models. Used in tests; production uses Alembic migrations."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
