from fastapi import APIRouter
from Application.APIs.users import router as users_router
from Application.APIs import users, recipes

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(recipes.router)