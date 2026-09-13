from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from later_api.api.deps import SessionDep
from later_api.exceptions import NotFoundError
from later_api.models.resources import ResourceStatus
from later_api.schemas.resources import ResourceCreate, ResourceEdit, ResourceRead
from later_api.services.resource_metadata_service.resource_metadata_service import (
    fetch_and_save_metadata,
)
from later_api.services.resources import create_resource as create_resource_service
from later_api.services.resources import delete_resource as delete_resource_service
from later_api.services.resources import edit_resource as edit_resource_service
from later_api.services.resources import (
    get_resource_by_id as get_resource_by_id_service,
)
from later_api.services.resources import get_resources as get_resources_service

router = APIRouter(prefix="/resources")


@router.post("", response_model=ResourceRead)
async def create_resource(
    resource: ResourceCreate,
    session: SessionDep,
    background_tasks: BackgroundTasks,
):
    """
    Accepts a URL, creates a Resource, then fetches title/source in the background.
    """
    created = create_resource_service(resource, session)
    if created.id is None:
        raise HTTPException(status_code=500, detail="Resource was not persisted")
    background_tasks.add_task(fetch_and_save_metadata, created.id, str(resource.url))
    return created


@router.get("", response_model=list[ResourceRead])
async def get_resources(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    status: ResourceStatus | None = None,
    source_id: int | None = None,
    category_id: int | None = None,
):
    """Return a paginated list of resources with optional filters."""
    return get_resources_service(
        session,
        offset,
        limit,
        status=status,
        source_id=source_id,
        category_id=category_id,
    )


@router.get("/{resource_id}", response_model=ResourceRead)
async def get_resource_by_id(resource_id: int, session: SessionDep):
    """Return a single resource by id."""
    try:
        return get_resource_by_id_service(resource_id, session)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/{resource_id}")
async def delete_resource(resource_id: int, session: SessionDep):
    """Delete a resource by id."""
    try:
        delete_resource_service(resource_id, session)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True}


@router.patch("/{resource_id}", response_model=ResourceRead)
async def edit_resource(resource_id: int, resource: ResourceEdit, session: SessionDep):
    """Update fields of an existing resource."""
    try:
        return edit_resource_service(resource_id, resource, session)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
