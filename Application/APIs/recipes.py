from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from Application.Database.session import get_db, get_read_db
from Application.Database.models.recipe import Recipe
from Application.Database.models.ingredient import Ingredient
from Application.Database.models.recipe_ingredient import RecipeIngredient

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/")
def get_recipes(db: Session = Depends(get_read_db)):
    return db.query(Recipe).all()

@router.get("/{recipe_id}")
def get_recipe(recipe_id: int, db: Session = Depends(get_read_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.post("/")
def create_recipe(
    title: str = Form(...),
    description: str = Form(...),
    instructions: str = Form(...),
    ingredients_str: str = Form(...),
    db: Session = Depends(get_db)
):
    new_recipe = Recipe(
        title=title,
        description=description,
        instructions=instructions,
        author_id=None
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    raw_ingredients = [i.strip() for i in ingredients_str.split(",") if i.strip()]
    for name in raw_ingredients:
        ingredient = db.query(Ingredient).filter(Ingredient.name == name).first()
        if not ingredient:
            ingredient = Ingredient(name=name, unit="pcs")
            db.add(ingredient)
            db.commit()
            db.refresh(ingredient)

        link = RecipeIngredient(
            recipe_id=new_recipe.id,
            ingredient_id=ingredient.id,
            quantity=0
        )
        db.add(link)
    
    db.commit()
    return RedirectResponse(url="/home", status_code=303)