from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Application.Database.session import get_db
from Application.Database.models.recipe import Recipe
from Application.Database.models.ingredient import Ingredient
from Application.Database.models.recipe_ingredient import RecipeIngredient
from Application.Schemas.recipe import RecipeCreate, RecipeResponse, IngredientResponse

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/", response_model=RecipeResponse)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):

    new_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        instructions=recipe.instructions,
        author_id=None
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    for item in recipe.ingredients:

        ingredient = db.query(Ingredient).filter(
            Ingredient.name == item.name
        ).first()

        if not ingredient:
            ingredient = Ingredient(
                name=item.name,
                unit="pcs"
            )
            db.add(ingredient)
            db.commit()
            db.refresh(ingredient)

        link = RecipeIngredient(
            recipe_id=new_recipe.id,
            ingredient_id=ingredient.id,
            quantity=item.quantity
        )

        db.add(link)

    db.commit()

    recipe_with_links = db.query(Recipe).filter(
        Recipe.id == new_recipe.id
    ).first()

    return RecipeResponse(
        id=recipe_with_links.id,
        title=recipe_with_links.title,
        description=recipe_with_links.description,
        instructions=recipe_with_links.instructions,
        created_at=recipe_with_links.created_at,
        ingredients=[
            IngredientResponse(
                name=ri.ingredient.name,
                quantity=ri.quantity
            )
            for ri in recipe_with_links.ingredients
        ]
    )
