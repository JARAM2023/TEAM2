from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import expression as sql_exp

from app import models as m
from app.utils.rdb import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


class login_user(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class signup_user(BaseModel):
    username: str
    password: str
    height: float
    weight: float
    gender: int

    class Config:
        orm_mode = True


@router.post("/signup")
def signup(item: signup_user):
    if any(existing_user.username == item.username for existing_user in m.User):
        raise HTTPException(status_code=400, detail="Username already taken")
    else:
        return JsonResponse(item, status=status.HTTP_201_CREATED)


@router.post("/login")
def login(item: login_user):
    match_user = [u for u in m.User if u.username == item.username]
    if not matched_user:
        raise HTTPException(status_code=401, detail="Login denied")
    if item.password != match_user[0].password:
        raise HTTPException(status_code=401, detail="Login denied")

    return {"message": "Login successful"}
