from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user():
    return {"message": "user created"}