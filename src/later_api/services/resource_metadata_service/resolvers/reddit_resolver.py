import json
from typing import override
from urllib.parse import urlparse

import requests
from sqlalchemy.sql.schema import MetaData

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
        metadata = ResourceMetadata(title=title, source="reddit")
        return metadata

    @staticmethod
    def parse_url(url: str) -> str:
        # добавляем схему, если её нет, чтобы netloc заполнился
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
            response.raise_for_status()  # Проверка на HTTP-ошибки

            data = response.json()  # pyright: ignore[reportAny]
            return data.get("title", "Заголовок не найден")  # pyright: ignore[reportAny]

        except requests.exceptions.RequestException as e:
            return f"Ошибка запроса: {e}"
        except json.JSONDecodeError:
            return "Ошибка: неверный формат ответа"
