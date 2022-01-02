from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/jokes/", response_model=schemas.Jokes)
def create_a_joke(dad: schemas.JokesCreate, db: Session = Depends(get_db)):
    db_jokes = crud.get_jokes_by_jokes(db=db, jokes=dad.jokes)
    if db_jokes:
        raise HTTPException(status_code=400, detail="Jokes already submitted")
    return crud.create_a_joke(db=db, dad=dad)


@app.get("/jokes/", response_model=List[schemas.Jokes])
def get_jokes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_jokes = crud.get_jokes(db=db, skip=skip, limit=limit)
    return db_jokes