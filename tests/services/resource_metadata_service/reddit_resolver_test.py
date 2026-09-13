from later_api.services.resource_metadata_service.resolvers.reddit_resolver import (
    RedditResolver,
)


def test_can_create_resolver() -> None:
    resolver = RedditResolver()
    assert resolver is not None


def test_can_resolve_reddit_url() -> None:
    resolver = RedditResolver()
    assert resolver.can_resolve("https://reddit.com/r/python") is True


def test_can_resolve_www_reddit_url() -> None:
    resolver = RedditResolver()
    assert resolver.can_resolve("https://www.reddit.com/r/python") is True


def test_can_resolve_google_url() -> None:
    resolver = RedditResolver()
    assert resolver.can_resolve("https://google.com") is False
