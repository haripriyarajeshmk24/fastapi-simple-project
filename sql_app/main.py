from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from . import crud,models,schemas
from .database import  SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users=crud.get_users(db=db)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db,user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="No user with given ID")
    return db_user

@app.post("/users/{user_id}/items", response_model=schemas.Item, status_code=201)
def create_item_for_user(user_id: int,item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    print(db_user)
    if db_user is None:
        print("entered if condition")
        raise HTTPException(status_code=400, detail="User Doesn't EXist!")
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip:int = 1, limit:int = 100, db: Session = Depends(get_db)):
    items=crud.get_items(db=db, skip=skip, limit=limit)
    return items

@app.delete("/{user_id}/", response_model=schemas.User)
def delete_item(user_id: int,db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user=user_id)


@app.delete("/users/{user_id}/items/{item_id}/", response_model=schemas.Item)
def delete_user_item(user_id: int, item_id: int, db: Session = Depends(get_db)):
    return crud.delete_user_item(db=db, item_id=item_id, user_id=user_id)

@app.put("/users/{user_id}", response_model=schemas.User)
def edit_user_status(user_id: int, db: Session = Depends(get_db)):
    return crud.edit_user_status(db=db, user_id=user_id)

@app.put("/users/{user_id}/items/{item_id}/", response_model=schemas.Item)
def edit_item_description(user_id: int, item_id: int, db: Session = Depends(get_db)):
    return crud.edit_item_description(db=db, item_id=item_id, user_id=user_id)