from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class IngredientInput(BaseModel):
    name: str = Field(..., min_length=1)
    quantity: float = Field(..., gt=0)


class RecipeBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    instructions: str = Field(..., min_length=5)


class RecipeCreate(RecipeBase):
    ingredients: List[IngredientInput]


class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    ingredients: Optional[List[IngredientInput]] = None


class IngredientResponse(BaseModel):
    name: str
    quantity: float

    class Config:
        from_attributes = True


class RecipeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    instructions: str
    created_at: Optional[datetime]
    ingredients: List[IngredientResponse]

    class Config:
        from_attributes = True
