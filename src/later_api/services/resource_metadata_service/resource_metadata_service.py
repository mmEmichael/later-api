import logging

from sqlmodel import Session, select

from later_api.database.database import engine
from later_api.exceptions import MetadataResolutionError
from later_api.models.resources import Resource
from later_api.models.sources import Source
from later_api.services.resource_metadata_service.resolvers.reddit_resolver import (
    RedditResolver,
)
from later_api.services.resource_metadata_service.resolvers.youtube_resolver import (
    YoutubeResolver,
)
from later_api.services.resource_metadata_service.resource_metadata import (
    ResourceMetadata,
)

logger = logging.getLogger(__name__)

resolvers = [
    RedditResolver(),
    YoutubeResolver(),
]


def find_resolver(url: str):
    for resolver in resolvers:
        if resolver.can_resolve(url):
            return resolver
    return None


def resolve_resource(url: str) -> ResourceMetadata | None:
    resolver = find_resolver(url)
    if resolver is None:
        logger.info("No metadata resolver found for url=%s", url)
        return None
    return resolver.resolve(url)


def save_metadata(resource_id: int, metadata: ResourceMetadata) -> None:
    """
    Background job: save metadata on Resource and create Source if needed.
    """
    with Session(engine) as session:
        resource = session.get(Resource, resource_id)
        if resource is None:
            logger.warning(
                "Cannot save metadata: resource_id=%s not found", resource_id
            )
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
        logger.info(
            "Saved metadata for resource_id=%s title=%r source=%s",
            resource_id,
            metadata.title,
            metadata.source,
        )


def fetch_and_save_metadata(resource_id: int, url: str) -> None:
    """
    Background job: resolve metadata for a URL and persist it.
    """
    try:
        metadata = resolve_resource(url)
    except MetadataResolutionError:
        logger.exception(
            "Failed to resolve metadata for resource_id=%s url=%s",
            resource_id,
            url,
        )
        return

    if metadata is None:
        return

    save_metadata(resource_id, metadata)
