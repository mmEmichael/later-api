from abc import ABC, abstractmethod

from later_api.services.resource_metadata_service.resource_metadata import (
    ResourceMetadata,
)


class ResourceResolver(ABC):
    @abstractmethod
    def can_resolve(self, url: str) -> bool:
        pass

    @abstractmethod
    def resolve(self, url: str) -> ResourceMetadata:
        pass
