from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud,models,schemas
from .database import  SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI

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

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db,user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="No user with given ID")
    return db_user