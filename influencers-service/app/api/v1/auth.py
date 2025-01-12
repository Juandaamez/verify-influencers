from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.security import verify_password, create_access_token, pwd_context
from app.db.session import get_db
from app.db.models import User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login", tags=["Auth"])
def login(
    db: Session = Depends(get_db),
    login_data: LoginRequest = Body(...),
):
    
    username = login_data.username
    password = login_data.password

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", tags=["Auth"])
def register(
    register_data: LoginRequest,
    db: Session = Depends(get_db),
):
    
    user = db.query(User).filter(User.username == register_data.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = pwd_context.hash(register_data.password)
    new_user = User(username=register_data.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully!"}
