from later_api.services.resource_metadata_service.resolvers.reddit_resolver import (
    RedditResolver,
)
from later_api.services.resource_metadata_service.resource_metadata import (
    ResourceMetadata,
)

resolvers = [
    RedditResolver(),
]


def find_resolver(url: str):
    for resolver in resolvers:
        if resolver.can_resolve(url):
            return resolver

    return None


def resolve_resource(url: str):
    resolver = find_resolver(url)

    if resolver is None:
        return None

    return resolver.resolve(url)


# later_api/services/resource_metadata_service/resource_metadata_service.py

from sqlmodel import Session, select

from later_api.database.database import engine
from later_api.models.resources import Resource
from later_api.models.sources import Source
from later_api.services.resource_metadata_service.resource_metadata import (
    ResourceMetadata,
)


def save_metadata(resource_id: int, metadata: ResourceMetadata) -> None:
    """
    Синхронная фоновая задача: сохраняет метаданные в Resource и
    при необходимости создаёт Source.
    """
    with Session(engine) as session:
        resource = session.get(Resource, resource_id)
        if resource is None:
            # логируй, а не молчи
            return

        resource.title = metadata.title

        source = session.exec(
            select(Source).where(Source.name == metadata.source)
        ).first()
        if source is None:
            source = Source(name=metadata.source)
            session.add(source)
            session.flush()

        resource.source_id = source.id

        session.add(resource)
        session.commit()


def fetch_and_save_metadata(resource_id: int, url: str) -> None:
    """
    Фоновая задача: резолвит метаданные по URL и сохраняет их.
    """
    metadata = resolve_resource(url)
    if metadata is None:
        return

    save_metadata(resource_id, metadata)
