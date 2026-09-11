import pytest

from later_api.exceptions import MetadataResolutionError
from later_api.services.resource_metadata_service.resolvers.reddit_resolver import (
    RedditResolver,
)
from later_api.services.resource_metadata_service.resource_metadata_service import (
    find_resolver,
    resolve_resource,
)


def test_find_resolver_for_reddit():
    url = "https://www.reddit.com/r/coolgithubprojects/comments/1w0uosa/opensource_capcut_alternative/"
    assert isinstance(find_resolver(url), RedditResolver)


def test_resolve_resource_for_reddit():
    url = "https://www.reddit.com/r/coolgithubprojects/comments/1w0uosa/opensource_capcut_alternative/"
    try:
        result = resolve_resource(url)
    except MetadataResolutionError:
        pytest.skip("Reddit oEmbed unavailable")
    assert result is not None
    assert result.source == "reddit"
    assert result.title
