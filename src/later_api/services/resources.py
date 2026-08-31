from sqlmodel import Session, select

from later_api.models.resources import Resource
from later_api.schemas.resources import ResourceCreate


def create_resouce(resource: ResourceCreate, session: Session):
    db_resource = Resource.model_validate(resource)

    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource


def read_resources(session: Session, offset: int, limit: int):
    resources = session.exec(select(Resource).offset(offset).limit(limit)).all()
    return resources
