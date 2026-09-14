from later_api.services.resource_metadata_service.resolvers.youtube_resolver import (
    YoutubeResolver,
)


def test_can_create_resolver() -> None:
    resolver = YoutubeResolver()
    assert resolver is not None


def test_can_resolve_reddit_url() -> None:
    resolver = YoutubeResolver()
    assert resolver.can_resolve("https://www.youtube.com/watch?v=ZGgtgkuT_AU") is True


def test_can_resolve_www_reddit_url() -> None:
    resolver = YoutubeResolver()
    assert resolver.can_resolve("https://www.youtube.com/watch?v=ZGgtgkuT_AU") is True


def test_can_resolve_google_url() -> None:
    resolver = YoutubeResolver()
    assert resolver.can_resolve("https://google.com") is False
