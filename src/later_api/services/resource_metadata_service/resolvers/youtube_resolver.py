from typing import override
from urllib.parse import urlparse

import requests

from later_api.exceptions import MetadataResolutionError
from later_api.services.resource_metadata_service.resolvers.base import ResourceResolver
from later_api.services.resource_metadata_service.resource_metadata import (
    ResourceMetadata,
)

YOUTUBE_HOSTS = ("youtube.com", "youtu.be")


class YoutubeResolver(ResourceResolver):
    @override
    def can_resolve(self, url: str) -> bool:
        if not url:
            return False
        host = self.parse_url(url).lower()
        return host in YOUTUBE_HOSTS or host.endswith(
            tuple("." + h for h in YOUTUBE_HOSTS)
        )

    @override
    def resolve(self, url: str) -> ResourceMetadata:
        title = self.get_youtube_title(url)
        return ResourceMetadata(title=title, source="youtube")

    @staticmethod
    def parse_url(url: str) -> str:
        if "://" not in url:
            url = "https://" + url
        return urlparse(url).netloc

    @staticmethod
    def get_youtube_title(url: str) -> str:
        endpoint = "https://www.youtube.com/oembed"
        params = {"url": url, "format": "json"}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        try:
            response = requests.get(
                endpoint, params=params, headers=headers, timeout=10
            )
            response.raise_for_status()
            data = response.json()  # pyright: ignore[reportAny]
        except requests.exceptions.RequestException as exc:
            raise MetadataResolutionError(
                f"Youtube oEmbed request failed for {url}"
            ) from exc
        except ValueError as exc:
            raise MetadataResolutionError(
                f"Youtube oEmbed returned invalid JSON for {url}"
            ) from exc

        title = data.get("title")  # pyright: ignore[reportAny]
        if not title or not isinstance(title, str):
            raise MetadataResolutionError(
                f"Youtube oEmbed response has no title for {url}"
            )
        return title
