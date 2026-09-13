import pytest
from sqlmodel import Session, select

from later_api.models.resources import Resource
from later_api.models.sources import Source
from later_api.services.resource_metadata_service.resource_metadata import (
    ResourceMetadata,
)
from later_api.services.resource_metadata_service.resource_metadata_service import (
    save_metadata,
)


def test_save_metadata_updates_resource_and_creates_source(
    session: Session,
    engine,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "later_api.services.resource_metadata_service.resource_metadata_service.engine",
        engine,
    )

    resource = Resource(url="https://www.reddit.com/r/python/comments/abc/hello/")
    session.add(resource)
    session.commit()
    session.refresh(resource)
    assert resource.id is not None

    save_metadata(
        resource.id,
        ResourceMetadata(title="Hello Reddit", source="reddit"),
    )

    session.expire_all()
    updated = session.get(Resource, resource.id)
    assert updated is not None
    assert updated.title == "Hello Reddit"
    assert updated.source_id is not None

    source = session.exec(select(Source).where(Source.name == "reddit")).first()
    assert source is not None
    assert updated.source_id == source.id


def test_save_metadata_missing_resource_does_not_crash(
    engine,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "later_api.services.resource_metadata_service.resource_metadata_service.engine",
        engine,
    )

    save_metadata(999, ResourceMetadata(title="Nope", source="reddit"))
