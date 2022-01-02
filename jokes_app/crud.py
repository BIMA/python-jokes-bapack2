from sqlalchemy.orm import Session

from . import models, schemas


def get_jokes_by_jokes(db: Session, jokes: str):
    return db.query(models.Jokes).filter(models.Jokes.jokes == jokes).first()


def get_jokes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Jokes).offset(skip).limit(limit).all()


def create_a_joke(db: Session, dad: schemas.JokesCreate):
    db_joke = models.Jokes(jokes=dad.jokes)
    db.add(db_joke)
    db.commit()
    db.refresh(db_joke)
    return db_joke
