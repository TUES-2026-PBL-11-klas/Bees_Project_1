from sqlalchemy.orm import Session
from sqlalchemy import func
from Application.Database.models import (
    Recipe,
    RecipeIngredient,
    UserIngredient
)


def smart_search_recipes(db: Session, user_id: int):
    missing_subquery = (
        db.query(
            Recipe.id.label("recipe_id"),
            func.count(RecipeIngredient.id).label("missing_count")
        )
        .join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id)
        .outerjoin(
            UserIngredient,
            (RecipeIngredient.ingredient_id == UserIngredient.ingredient_id)
            & (UserIngredient.user_id == user_id)
        )
        .filter(UserIngredient.id == None)
        .group_by(Recipe.id)
        .subquery()
    )

    query = (
        db.query(
            Recipe,
            func.coalesce(missing_subquery.c.missing_count, 0).label("missing_count")
        )
        .outerjoin(missing_subquery, Recipe.id == missing_subquery.c.recipe_id)
        .order_by("missing_count")
    )

    results = query.all()

    return [
        {
            "recipe_id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "missing_ingredients": missing_count
        }
        for recipe, missing_count in results
    ]
