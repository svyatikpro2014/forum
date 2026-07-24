from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_session
from models import UsersModel
from schemas import UserAddSchema, UserResponse
from passlib.context import CryptContext
from authx import AuthX, AuthXConfig, TokenPayload 
import os
from dotenv import load_dotenv


router = APIRouter(prefix="/auth", tags=["auth"])

load_dotenv()

config = AuthXConfig()

config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
config.JWT_TOKEN_LOCATION = ["headers"]
config.JWT_HEADER_NAME = "Authorization"
config.JWT_HEADER_TYPE = "Bearer"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = AuthX(config=config)


def hash_password(password:str) -> str:
    return pwd_context.hash(password)


def verify_password(password:str, hashed_password:str) -> bool:
    return pwd_context.verify(password, hashed_password)


@router.post("/registration", response_model=UserResponse)
async def register(user:UserAddSchema, session:AsyncSession = Depends(get_session)):
    check = await session.execute(select(UsersModel).where(UsersModel.email == user.email))
    exists = check.scalar_one_or_none()
    
    if exists:
        raise HTTPException(status_code=400, detail="email alredy used")
    
    hashed_password = hash_password(str(user.password))

    new_user = UsersModel(email=user.email, password=hashed_password, role=user.role)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.post("/login")
async def login(user:UserAddSchema, session:AsyncSession = Depends(get_session)):
    result = await session.execute(select(UsersModel).where(UsersModel.email == user.email))
    exists = result.scalar_one_or_none()

    if not exists:
        raise HTTPException(status_code=401, detail="User not found")
    
    if not verify_password(str(user.password), exists.password):
        raise HTTPException(status_code=401, detail="Wrong password")
    
    token = security.create_access_token(uid=str(exists.id))
    return {"access token": token, "type": "bearer"}



async def get_user(payload: TokenPayload = Depends(security.access_token_required), session: AsyncSession = Depends(get_session)):
    user_id = payload.sub

    result = await session.execute(select(UsersModel).where(UsersModel.id == int(user_id)))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_user)):
    return current_user