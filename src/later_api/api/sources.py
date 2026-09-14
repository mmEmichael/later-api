from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from later_api.api.deps import SessionDep
from later_api.exceptions import NotFoundError
from later_api.schemas.sources import SourceRead
from later_api.services.sources import get_source_by_id as get_source_by_id_service
from later_api.services.sources import get_sources as get_sources_service

router = APIRouter(prefix="/sources")


@router.get("", response_model=list[SourceRead])
async def get_sources(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    """Return a paginated list of sources."""
    return get_sources_service(session, offset, limit)


@router.get("/{source_id}", response_model=SourceRead)
async def get_source_by_id(source_id: int, session: SessionDep):
    """Return a single source by id."""
    try:
        return get_source_by_id_service(source_id, session)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
