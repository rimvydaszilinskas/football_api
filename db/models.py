from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import String, Integer, Column, Float

from .database import Base


class Player(Base):
    __tablename__ = 'footballers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    photo = Column(String)
    nationality = Column(String)
    overall = Column(Integer)
    club = Column(String)
    position = Column(String)
    value = Column(Float)


class PlayerSchema(BaseModel):
    """
    Model helper for serialization
    """
    id: int
    name: str
    age: int
    photo: Optional[str]
    nationality: str
    overall: int
    club: Optional[str]
    position: Optional[str]
    value: Optional[float]

    class Config:
        orm_mode = True


class BestTeamInputSchema(BaseModel):
    ammount: int
