from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.database_service import DatabaseService

router = APIRouter()
db = DatabaseService()

class CreateUserReq(BaseModel):
    username: str

@router.post("/create")
def create_user(req: CreateUserReq):
    user = db.get_user_by_username(req.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user_id = db.create_user(req.username)
    return {"user_id": user_id, "username": req.username}

@router.get("/{user_id}")
def get_user(user_id: int):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user