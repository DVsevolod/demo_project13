from pydantic import BaseModel


class Hero(BaseModel):
    name: str
    hp: int
    level: int
    exp: int


class User(BaseModel):
    username: str
    hero: Hero
