from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from later_api.database.database import SessionDep
from later_api.models.resources import Resource
from later_api.schemas.resources import ResourceCreate, ResourceEdit
from later_api.services.resource_metadata_service.resource_metadata_service import (
    fetch_and_save_metadata,
)
from later_api.services.resources import create_resouce as create_resource_service
from later_api.services.resources import delete_resource as delete_resource_service
from later_api.services.resources import edit_resource as edit_resource_service
from later_api.services.resources import get_resources as get_resources_service
from later_api.services.resources import (
    get_resources_by_id as get_resources_by_id_service,
)

router = APIRouter(prefix="/resources")


@router.post("", response_model=Resource)
async def create_resource(
    resource: ResourceCreate,
    session: SessionDep,
    background_tasks: BackgroundTasks,
):
    """
    1. принимает URL;
    2. определяет источник;
    3. создаёт Resource;
    4. добавляет его в Inbox.

    """
    created = create_resource_service(resource, session)
    if created.id is None:
        raise HTTPException(status_code=500, detail="Resource was not persisted")
    background_tasks.add_task(fetch_and_save_metadata, created.id, str(resource.url))
    return created


@router.get("")
async def get_resources(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    """
    Возвращает список ресурсов
    """
    return get_resources_service(session, offset, limit)


@router.get("/{resource_id}")
async def get_resources_by_id(resource_id: int, session: SessionDep):
    """
    Возвращает ресурс по id
    """
    return get_resources_by_id_service(resource_id, session)


@router.delete("/{resource_id}")
async def delete_resource(resource_id: int, session: SessionDep):
    """
    Удалаяет ресурс по id
    """
    return delete_resource_service(resource_id, session)


@router.patch("/")
async def edit_resource(resource: ResourceEdit, session: SessionDep):
    return edit_resource_service(resource, session)
