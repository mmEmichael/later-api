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
    result = resolve_resource(url)
    print(result)
    assert result is not None
