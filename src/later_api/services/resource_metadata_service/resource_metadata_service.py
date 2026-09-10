from later_api.services.resource_metadata_service.resolvers.reddit_resolver import (
    RedditResolver,
)

resolvers = [
    RedditResolver(),
]


def find_resolver(url: str):
    for resolver in resolvers:
        if resolver.can_resolve(url):
            return resolver

    return None


def resolve_resource(url: str):
    resolver = find_resolver(url)

    if resolver is None:
        return None

    return resolver.resolve(url)
