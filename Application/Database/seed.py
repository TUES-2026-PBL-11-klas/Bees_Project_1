from sqlalchemy.orm import Session
from Application.Database.session import SessionWrite
from Application.Database.models.recipe import Recipe
from Application.Database.models.ingredient import Ingredient
from Application.Database.models.recipe_ingredient import RecipeIngredient
from datetime import datetime

def seed():
    db: Session = SessionWrite()
    try:
        db.query(RecipeIngredient).delete()
        db.query(Recipe).delete()
        db.query(Ingredient).delete()
        db.commit()

        flour = Ingredient(name="Flour", unit="g")
        eggs = Ingredient(name="Eggs", unit="pcs")
        milk = Ingredient(name="Milk", unit="ml")
        sugar = Ingredient(name="Sugar", unit="g")
        butter = Ingredient(name="Butter", unit="g")
        chicken = Ingredient(name="Chicken", unit="g")
        rice = Ingredient(name="Rice", unit="g")
        salt = Ingredient(name="Salt", unit="g")

        db.add_all([flour, eggs, milk, sugar, butter, chicken, rice, salt])
        db.commit()

        pancake = Recipe(
            title="Pancakes",
            description="Classic breakfast pancakes",
            instructions="Mix ingredients and fry.",
            author_id=None,
            created_at=datetime.utcnow()
        )

        chicken_rice = Recipe(
            title="Chicken with Rice",
            description="Simple chicken and rice meal",
            instructions="Cook chicken and boil rice.",
            author_id=None,
            created_at=datetime.utcnow()
        )

        db.add_all([pancake, chicken_rice])
        db.commit()

        db.add_all([
            RecipeIngredient(recipe_id=pancake.id, ingredient_id=flour.id, quantity=200),
            RecipeIngredient(recipe_id=pancake.id, ingredient_id=eggs.id, quantity=2),
            RecipeIngredient(recipe_id=pancake.id, ingredient_id=milk.id, quantity=300),
            RecipeIngredient(recipe_id=pancake.id, ingredient_id=sugar.id, quantity=50),
            RecipeIngredient(recipe_id=chicken_rice.id, ingredient_id=chicken.id, quantity=300),
            RecipeIngredient(recipe_id=chicken_rice.id, ingredient_id=rice.id, quantity=200),
            RecipeIngredient(recipe_id=chicken_rice.id, ingredient_id=salt.id, quantity=5),
        ])
        db.commit()
        print("Ingredients and recipes seeded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()