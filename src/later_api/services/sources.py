from sqlmodel import Session, select

from later_api.exceptions import NotFoundError
from later_api.models.sources import Source


def get_sources(session: Session, offset: int, limit: int) -> list[Source]:
    return list(session.exec(select(Source).offset(offset).limit(limit)).all())


def get_source_by_id(source_id: int, session: Session) -> Source:
    source = session.get(Source, source_id)
    if not source:
        raise NotFoundError(f"Source {source_id} not found")
    return source
