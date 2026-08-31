from fastapi import APIRouter

from later_api.database.database import SessionDep
from later_api.models.resources import Resource
from later_api.schemas.resources import ResourceCreate
from later_api.services.resources import create_resouce as create_resource_service

router = APIRouter(prefix="/resources")


@router.post("", response_model=Resource)
async def create_resource(resource: ResourceCreate, session: SessionDep):
    """
    Backend:
    1. принимает URL;
    2. определяет источник;
    3. создаёт Resource;
    4. добавляет его в Inbox.

    """
    return create_resource_service(resource, session)
