
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi import APIRouter
from Application.APIs.users import router as users_router
from Application.APIs import users, recipes

router = APIRouter()
templates = Jinja2Templates(directory="Application/Templates")


# MOCK DATABASE
recipes_db = [
    {
        "name": "Omelette",
        "ingredients": ["eggs", "milk", "cheese"],
        "description": "Simple fluffy omelette."
    },
    {
        "name": "Pancakes",
        "ingredients": ["milk", "flour", "eggs"],
        "description": "Classic breakfast pancakes."
    },
    {
        "name": "Salad",
        "ingredients": ["tomato", "cucumber", "cheese"],
        "description": "Fresh healthy salad."
    },
]


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/search", response_class=HTMLResponse)
async def search(request: Request, ingredients: str = Form(...)):

    user_ingredients = [i.strip().lower() for i in ingredients.split(",")]

    results = []

    for recipe in recipes_db:
        missing = [i for i in recipe["ingredients"] if i not in user_ingredients]

        results.append({
            "name": recipe["name"],
            "description": recipe["description"],
            "ingredients": recipe["ingredients"],
            "missing": missing
        })

    results.sort(key=lambda x: len(x["missing"]))

    return templates.TemplateResponse("results.html", {
        "request": request,
        "recipes": results
    })


@router.get("/add-recipe", response_class=HTMLResponse)
async def add_recipe_page(request: Request):
    return templates.TemplateResponse("add_recipe.html", {"request": request})


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

api_router.include_router(users.router)
api_router.include_router(recipes.router)

