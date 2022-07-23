from fastapi import APIRouter, Response, Depends
from typing import Union
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.database import get_db

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .models import User
from .schemas import LoginSchema, UserOut, Token, AccessToken
from .crud import (create_user, get_user_by_username, verify_password, create_access_token, get_current_user, create_refresh_token, create_access_token_with_refresh_token)
from config.schemas import Message
from config import settings

router = APIRouter(
    prefix="",
    tags=["Authentication"],
    responses={404: {"message": "Not found"}},
)

@router.post('/login', response_model=Union[Token, Message])
def login(user: LoginSchema, response: Response, db: Session=Depends(get_db)):

    _user = get_user_by_username(db, user.username)

    if not _user:
        _user = create_user(db, user)
    else:
        if not verify_password(user.password, _user.hashed_password):
            response.status_code = 400
            response.response_model = Message
            return {"message": "Please provide valid Credentials"}
    
    # 
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # JWT access Token generate
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )

    _user.access_token = access_token
    return _user


@router.post('/token', tags=['Token'])
async def login_for_access_token(response: Response, db: Session=Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    _user = get_user_by_username(db, form_data.username)
    if not _user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    else:
        if not verify_password(form_data.password, _user.hashed_password):
            response.status_code = 400
            response.response_model = Message
            return {"message": "Please provide valid Credentials"}

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": _user.username}, expires_delta=access_token_expires
    )

    refresh_token = create_refresh_token(data={"username": _user.username})
    return {"access_token": str(access_token), "token_type": "bearer", 'refresh_token': str(refresh_token)}


@router.post('/token/refresh',tags=['Token'], response_model=Union[AccessToken])
def refresh(refresh_token: str, response: Response, db: Session=Depends(get_db)):
    access_token = create_access_token_with_refresh_token(refresh_token)
    return {"access_token": str(access_token)}


@router.post('/profile', response_model=Union[UserOut])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

