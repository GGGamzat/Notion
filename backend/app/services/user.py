from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.utils import hash_password, verify_password, create_access_token, check_email_unique
from datetime import timedelta
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def login_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Неправильный пароль")

    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


def register_user(user: UserCreate, db: Session):
    check_email_unique(db, user.email)
    hashed = hash_password(user.password)

    new_user = User(username=user.username, email=user.email, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user