from sqlalchemy.orm import Session

from models import MenuItem
from schema import NewItems


def add_item(item: NewItems, db: Session):
    result = db.query(MenuItem).filter(MenuItem.dish_code == item.dish_code).first()

    if result is not None:
        return 1

    new_item = MenuItem(
        dish_code=item.dish_code,
        dish_name=item.dish_name,
        calorie_count=item.calorie_count,
        price=item.price,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


def get_all(db: Session):
    result = db.query(MenuItem).all()

    return result


def get_item_by_id(item_id: int, db: Session):
    result = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if result is None:
        return None

    return result


def update_item_by_id(item_id: int, item: NewItems, db: Session):
    result = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if result is None:
        return None

    result.dish_code = item.dish_code
    result.dish_name = item.dish_name
    result.calorie_count = item.calorie_count
    result.price = item.price

    db.commit()
    db.refresh(result)

    return result


def delete_item_by_id(item_id: int, db: Session):
    result = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if result is None:
        return None

    del_item = result

    db.delete(result)
    db.commit()

    return del_item
