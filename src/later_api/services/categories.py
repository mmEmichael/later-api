from sqlmodel import Session, select

from later_api.exceptions import NotFoundError
from later_api.models.categories import Category
from later_api.schemas.categories import CategoryCreate, CategoryEdit


def create_category(category: CategoryCreate, session: Session) -> Category:
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


def get_categories(session: Session, offset: int, limit: int) -> list[Category]:
    return list(session.exec(select(Category).offset(offset).limit(limit)).all())


def get_category_by_id(category_id: int, session: Session) -> Category:
    category = session.get(Category, category_id)
    if not category:
        raise NotFoundError(f"Category {category_id} not found")
    return category


def delete_category(category_id: int, session: Session) -> None:
    category = session.get(Category, category_id)
    if not category:
        raise NotFoundError(f"Category {category_id} not found")
    session.delete(category)
    session.commit()


def edit_category(
    category_id: int, category: CategoryEdit, session: Session
) -> Category:
    category_db = session.get(Category, category_id)
    if not category_db:
        raise NotFoundError(f"Category {category_id} not found")

    category_data = category.model_dump(exclude_unset=True)
    _ = category_db.sqlmodel_update(category_data)
    session.add(category_db)
    session.commit()
    session.refresh(category_db)
    return category_db
