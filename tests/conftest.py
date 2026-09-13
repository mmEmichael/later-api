from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import later_api.models  # noqa: F401 — register mappers  # pyright: ignore[reportUnusedImport]
from later_api.database.database import get_session
from later_api.main import app


@pytest.fixture(name="engine")
def engine_fixture() -> Generator:
    """In-memory SQLite shared across connections in one test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(
    engine, monkeypatch: pytest.MonkeyPatch
) -> Generator[TestClient, None, None]:
    """
    HTTP client against the real FastAPI app, but with:
    - test SQLite instead of Postgres
    - no schema create on the real DATABASE_URL
    - background metadata writing into the same test DB
    """

    def get_session_override() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    monkeypatch.setattr("later_api.main.create_db_and_tables", lambda: None)
    monkeypatch.setattr(
        "later_api.services.resource_metadata_service.resource_metadata_service.engine",
        engine,
    )

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
