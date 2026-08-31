from typing import Annotated

from fastapi import APIRouter, Query

from later_api.database.database import SessionDep
from later_api.models.resources import Resource
from later_api.schemas.resources import ResourceCreate, ResourceRead
from later_api.services.resources import create_resouce as create_resource_service
from later_api.services.resources import read_resources as read_resources_service

router = APIRouter(prefix="/resources")


@router.post("", response_model=Resource)
async def create_resource(resource: ResourceCreate, session: SessionDep):
    """
    1. принимает URL;
    2. определяет источник;
    3. создаёт Resource;
    4. добавляет его в Inbox.

    """
    return create_resource_service(resource, session)


@router.get("")
async def read_resources(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    """
    Возвращает список ресурсов
    """
    return read_resources_service(session, offset, limit)
