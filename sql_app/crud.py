from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db:Session, user:schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db:Session, skip:int = 0, limit: int =100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db:Session, item:schemas.ItemCreate, user_id:int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    print(db_item, "db_item")
    db.add(db_item)
    print("add successful")
    db.commit()
    print("commit successful")
    db.refresh(db_item)
    return db_item


def delete_user(db:Session, user:int):
    db_item = db.query(models.User).filter(models.User.id == user).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_item)
    db.commit()
    return db_item


def delete_user_item(db: Session, item_id: int, user_id: int):
    db_item = (
        db.query(models.Item)
        .filter(models.Item.id == item_id, models.Item.owner_id == user_id)
        .first()
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found or access denied")
    db.delete(db_item)
    db.commit()
    return db_item


def edit_user_status(db: Session, user_id: int):
    db_user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.is_active = False
    db.commit()
    return db_user


def edit_item_description(db: Session, user_id: int, item_id: int):
    db_item = (
        db.query(models.Item)
        .filter(models.Item.id == item_id, models.Item.owner_id == user_id)
        .first()
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found or access denied")
    db_item.description = "Description Changed"
    db.commit()
    return db_item