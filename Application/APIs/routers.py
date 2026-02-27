from fastapi import APIRouter, Request, Form, Depends, HTTPException, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
#import jwt

from Application.Database.session import get_db, get_read_db
from Application.Database.models.user import User
from Application.Database.models.recipe import Recipe
from Application.APIs import users as users_api, recipes as recipes_api
from Application.Core.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

api_router = APIRouter()
templates = Jinja2Templates(directory="Application/Templates")

@api_router.get("/home", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_read_db)):
    db_recipes = db.query(Recipe).order_by(Recipe.created_at.desc()).limit(12).all()
    return templates.TemplateResponse("home.html", {"request": request, "recipes": db_recipes})

@api_router.post("/search", response_class=HTMLResponse)
async def search(request: Request, ingredients: str = Form(...), db: Session = Depends(get_read_db)):
    user_ingredients = set(i.strip().lower() for i in ingredients.split(",") if i.strip())
    all_recipes = db.query(Recipe).all()
    results = []
    for recipe in all_recipes:
        recipe_ing_names = set(ri.ingredient.name.lower() for ri in recipe.ingredients)
        missing = list(recipe_ing_names - user_ingredients)
        matches = recipe_ing_names.intersection(user_ingredients)
        if matches:
            results.append({
                "name": recipe.title,
                "description": recipe.description,
                "ingredients": list(recipe_ing_names),
                "missing": missing,
                "match_count": len(matches)
            })
    results.sort(key=lambda x: (-x["match_count"], len(x["missing"])))
    return templates.TemplateResponse("results.html", {"request": request, "recipes": results[:20]})

@api_router.post("/register")
async def register(
    request: Request,
    username: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    user_exists = db.query(User).filter(User.username == username).first()
    if user_exists:
        return HTMLResponse("User already exists", status_code=400)
    
    new_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.username})
    response = RedirectResponse(url="/profile", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    
    return response

@api_router.post("/login")
async def login(
    request: Request,
    username: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_read_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return HTMLResponse("Invalid credentials", status_code=401)
    
    access_token = create_access_token(data={"sub": user.username})
    
    response = RedirectResponse(url="/profile", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    
    return response

@api_router.get("/add-recipe", response_class=HTMLResponse)
async def add_recipe_page(request: Request):
    return templates.TemplateResponse("add_recipe.html", {"request": request})

#@api_router.get("/profile", response_class=HTMLResponse)
#async def profile_page(request: Request, current_user: User = Depends(get_current_user_from_cookie)):
    #return templates.TemplateResponse("profile.html", {"request": request, "current_user": current_user})

api_router.include_router(recipes_api.router)
api_router.include_router(users_api.router)