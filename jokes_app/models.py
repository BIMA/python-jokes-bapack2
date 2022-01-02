from sqlalchemy import Column, Integer, String
from .database import Base


class Jokes(Base):
    __tablename__ = "jokes"

    id = Column(Integer, primary_key=True, index=True)
    jokes = Column(String)
