from pydantic import BaseModel


class JokesBase(BaseModel):
    jokes: str


class JokesCreate(JokesBase):
    pass


class Jokes(JokesBase):
    id: int

    class Config:
        orm_mode = True
