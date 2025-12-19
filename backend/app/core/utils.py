from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
import bcrypt
from datetime import datetime
from jose import jwt

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def hash_password(password: str) -> str:
    # Преобразуем пароль в байты
    password_bytes = password.encode('utf-8')
    # Хешируем с bcrypt
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Возвращаем строку для хранения в базе
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def check_email_unique(db: Session, email: str):
    if db.query(User).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже существует")