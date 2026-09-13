from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from later_api.api.deps import SessionDep
from later_api.exceptions import NotFoundError
from later_api.schemas.categories import CategoryCreate, CategoryEdit, CategoryRead
from later_api.services.categories import create_category as create_category_service
from later_api.services.categories import delete_category as delete_category_service
from later_api.services.categories import edit_category as edit_category_service
from later_api.services.categories import (
    get_categories as get_categories_service,
)
from later_api.services.categories import (
    get_category_by_id as get_category_by_id_service,
)

router = APIRouter(prefix="/categories")


@router.post("", response_model=CategoryRead)
async def create_category(category: CategoryCreate, session: SessionDep):
    """Create a new category."""
    created = create_category_service(category, session)
    if created.id is None:
        raise HTTPException(status_code=500, detail="Category was not persisted")
    return created


@router.get("", response_model=list[CategoryRead])
async def get_categories(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    """Return a paginated list of categories."""
    return get_categories_service(session, offset, limit)


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category_by_id(category_id: int, session: SessionDep):
    """Return a single category by id."""
    try:
        return get_category_by_id_service(category_id, session)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/{category_id}", response_model=CategoryRead)
async def edit_category(
    category_id: int, category: CategoryEdit, session: SessionDep
):
    """Update an existing category."""
    try:
        return edit_category_service(category_id, category, session)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/{category_id}")
async def delete_category(category_id: int, session: SessionDep):
    """Delete a category by id."""
    try:
        delete_category_service(category_id, session)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True}
