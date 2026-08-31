from fastapi import HTTPException
from sqlmodel import Session, select

from later_api.models.resources import Resource
from later_api.schemas.resources import ResourceCreate, ResourceEdit


def create_resouce(resource: ResourceCreate, session: Session):
    db_resource = Resource.model_validate(resource)

    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource


def get_resources(session: Session, offset: int, limit: int):
    resources = session.exec(select(Resource).offset(offset).limit(limit)).all()
    return resources


def get_resources_by_id(id: int, session: Session):
    resource = session.get(Resource, id)
    if not resource:
        raise HTTPException(status_code=404, detail="Hero not found")
    return resource


def delete_resource(id: int, session: Session):
    resource = session.get(Resource, id)
    if not resource:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(resource)
    session.commit()
    return {"ok": True}


def edit_resource(resource: ResourceEdit, session: Session):
    resource_db = session.get(Resource, resource.id)
    if not resource_db:
        raise HTTPException(status_code=404, detail="Resource not found")
    resource_data = resource.model_dump(exclude_unset=True)
    _ = resource_db.sqlmodel_update(resource_data)
    session.add(resource_db)
    session.commit()
    session.refresh(resource_db)
    return resource_db
