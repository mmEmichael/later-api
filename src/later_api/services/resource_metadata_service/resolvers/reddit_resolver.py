from typing import override
from urllib.parse import urlparse

import requests

from later_api.exceptions import MetadataResolutionError
from later_api.services.resource_metadata_service.resolvers.base import ResourceResolver
from later_api.services.resource_metadata_service.resource_metadata import (
    ResourceMetadata,
)

REDDIT_HOST = "reddit.com"


class RedditResolver(ResourceResolver):
    @override
    def can_resolve(self, url: str) -> bool:
        if not url:
            return False
        host = self.parse_url(url).lower()
        return host == REDDIT_HOST or host.endswith("." + REDDIT_HOST)

    @override
    def resolve(self, url: str) -> ResourceMetadata:
        title = self.get_reddit_title(url)
        return ResourceMetadata(title=title, source="reddit")

    @staticmethod
    def parse_url(url: str) -> str:
        if "://" not in url:
            url = "https://" + url
        return urlparse(url).netloc

    @staticmethod
    def get_reddit_title(url: str) -> str:
        endpoint = "https://www.reddit.com/oembed"
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
                f"Reddit oEmbed request failed for {url}"
            ) from exc
        except ValueError as exc:
            raise MetadataResolutionError(
                f"Reddit oEmbed returned invalid JSON for {url}"
            ) from exc

        title = data.get("title")  # pyright: ignore[reportAny]
        if not title or not isinstance(title, str):
            raise MetadataResolutionError(
                f"Reddit oEmbed response has no title for {url}"
            )
        return title
