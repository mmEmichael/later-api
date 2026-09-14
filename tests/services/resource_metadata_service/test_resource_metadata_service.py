from unittest.mock import MagicMock

import pytest

from later_api.exceptions import MetadataResolutionError
from later_api.services.resource_metadata_service.resolvers.reddit_resolver import (
    RedditResolver,
)
from later_api.services.resource_metadata_service.resource_metadata_service import (
    find_resolver,
    resolve_resource,
)


def test_find_resolver_for_reddit() -> None:
    url = "https://www.reddit.com/r/python/comments/abc/hello/"
    assert isinstance(find_resolver(url), RedditResolver)


def test_resolve_resource_with_mocked_reddit(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_response = MagicMock()
    fake_response.raise_for_status = MagicMock()
    fake_response.json.return_value = {"title": "Open source CapCut alternative"}

    monkeypatch.setattr(
        "later_api.services.resource_metadata_service.resolvers.reddit_resolver.requests.get",
        MagicMock(return_value=fake_response),
    )

    url = "https://www.reddit.com/r/python/comments/abc/hello/"
    result = resolve_resource(url)

    assert result is not None
    assert result.source == "reddit"
    assert result.title == "Open source CapCut alternative"


def test_resolve_resource_raises_on_request_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import requests

    monkeypatch.setattr(
        "later_api.services.resource_metadata_service.resolvers.reddit_resolver.requests.get",
        MagicMock(side_effect=requests.exceptions.Timeout("boom")),
    )

    url = "https://www.reddit.com/r/python/comments/abc/hello/"
    with pytest.raises(MetadataResolutionError):
        resolve_resource(url)


def test_resolve_resource_raises_when_title_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_response = MagicMock()
    fake_response.raise_for_status = MagicMock()
    fake_response.json.return_value = {}

    monkeypatch.setattr(
        "later_api.services.resource_metadata_service.resolvers.reddit_resolver.requests.get",
        MagicMock(return_value=fake_response),
    )

    url = "https://www.reddit.com/r/python/comments/abc/hello/"

    with pytest.raises(MetadataResolutionError):
        resolve_resource(url)
