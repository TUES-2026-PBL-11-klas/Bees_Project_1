from pydantic import BaseModel


class FavoriteCreate(BaseModel):
    recipe_id: int


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    recipe_id: int

    class Config:
        orm_mode = True