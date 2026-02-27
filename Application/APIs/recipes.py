from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Application.Database.session import get_db
from Application.Database.models import Recipe
from Application.Core.recipe_service import smart_search_recipes

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/")
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).all()


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


@router.post("/")
def create_recipe(recipe: dict, db: Session = Depends(get_db)):
    new_recipe = Recipe(**recipe)
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


@router.get("/smart-search/{user_id}")
def smart_search(user_id: int, db: Session = Depends(get_db)):
    return smart_search_recipes(db, user_id)
