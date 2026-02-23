from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class RecipeBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=5)
    ingredients: List[str]


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    ingredients: Optional[List[str]]


class RecipeResponse(RecipeBase):
    id: int
    owner_id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True