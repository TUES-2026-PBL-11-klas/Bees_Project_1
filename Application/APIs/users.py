from fastapi import APIRouter
from typing import List
from Application.Schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    return {"id": 1, "email": user.email}

@router.get("/", response_model=List[UserResponse])
def get_users():
    return [{"id": 1, "email": "test@example.com"}]

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return {"id": user_id, "email": "test@example.com"}