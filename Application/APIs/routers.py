from fastapi import APIRouter
from Application.APIs.users import router as users_router

api_router = APIRouter()

api_router.include_router(users_router)