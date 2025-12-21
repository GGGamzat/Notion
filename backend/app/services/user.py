from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.database import get_db
from app.schemas.user import UserCreate
from app.core.utils import hash_password, verify_password, create_access_token, check_email_unique
from datetime import timedelta
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def login_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Неправильный пароль")

    access_token = create_access_token(
        # data={"sub": user.id},
        data={"sub": str(user.id)},
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


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        
        if user is None:
            raise credentials_exception
        
        return user
    
    except JWTError:
        raise credentials_exception