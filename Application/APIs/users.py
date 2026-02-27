from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import or_

from Application.Database.session import get_db
from Application.Database.models.user import User
from Application.Schemas.user import UserCreate, UserResponse
from Application.Core.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
    or_(User.email == user.email, User.username == user.username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=user.hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

    


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
