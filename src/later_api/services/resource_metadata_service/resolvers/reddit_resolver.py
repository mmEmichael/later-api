from typing import override

from later_api.services.resource_metadata_service.resolvers.base import ResourceResolver
from later_api.services.resource_metadata_service.resouce_metadata import (
    ResourceMetadata,
)


class RedditResolver(ResourceResolver):
    @override
    def can_resolve(self, url: str) -> bool: ...

    @override
    def resolve(self, url: str) -> ResourceMetadata: ...
