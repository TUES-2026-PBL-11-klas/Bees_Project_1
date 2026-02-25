from fastapi import APIRouter

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/")
def get_recipes():
    return [{"id": 1, "title": "Test Recipe"}]

@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    return {"id": recipe_id, "title": "Test Recipe"}

@router.post("/")
def create_recipe():
    return {"message": "recipe created"}