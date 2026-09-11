from sqlmodel import Session, select

from later_api.exceptions import NotFoundError
from later_api.models.resources import Resource
from later_api.schemas.resources import ResourceCreate, ResourceEdit


def create_resource(resource: ResourceCreate, session: Session) -> Resource:
    db_resource = Resource.model_validate(resource)

    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource


def get_resources(session: Session, offset: int, limit: int) -> list[Resource]:
    return list(session.exec(select(Resource).offset(offset).limit(limit)).all())


def get_resource_by_id(resource_id: int, session: Session) -> Resource:
    resource = session.get(Resource, resource_id)
    if not resource:
        raise NotFoundError(f"Resource {resource_id} not found")
    return resource


def delete_resource(resource_id: int, session: Session) -> None:
    resource = session.get(Resource, resource_id)
    if not resource:
        raise NotFoundError(f"Resource {resource_id} not found")
    session.delete(resource)
    session.commit()


def edit_resource(
    resource_id: int, resource: ResourceEdit, session: Session
) -> Resource:
    resource_db = session.get(Resource, resource_id)
    if not resource_db:
        raise NotFoundError(f"Resource {resource_id} not found")

    resource_data = resource.model_dump(exclude_unset=True)
    _ = resource_db.sqlmodel_update(resource_data)
    session.add(resource_db)
    session.commit()
    session.refresh(resource_db)
    return resource_db
