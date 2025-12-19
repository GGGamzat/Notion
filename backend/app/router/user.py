from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.core.database import get_db
from app.services.user import register_user, login_user
from app.models.user import User

auth_router = APIRouter()

@auth_router.post("/users/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user.email, user.password, db)

@auth_router.post("/users/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)


@auth_router.get("/users/{user_id:int}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return {"user_id": user.id, "username": user.username}