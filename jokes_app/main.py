import random
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/get_random_jokes/", response_model=schemas.Jokes)
def get_random_jokes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_jokes = crud.get_jokes(db=db, skip=skip, limit=limit)
    len_db = len(db_jokes)
    idx = random.randint(0, len_db)
    return db_jokes[idx]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
