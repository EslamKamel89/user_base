from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.params import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schema import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix='/users' , tags=['users'])

@router.post('' , response_model=UserRead , status_code=status.HTTP_200_OK)
async def create_user(payload:UserCreate , session:AsyncSession=Depends(get_session)) :
    repo = UserRepository(session)
    existing = await repo.get_by_email(payload.email)
    if existing is not None :
        raise HTTPException(status.HTTP_409_CONFLICT , 'email already exists')
    user = await repo.create(name=payload.name , email=payload.email , password=payload.password)
    return user

@router.get('/{user_id}'  , response_model=UserRead , status_code=status.HTTP_200_OK)
async def get_user(user_id:Annotated[int , Path(ge=1)] , session:AsyncSession=Depends(get_session)) :
    repo = UserRepository(session)
    user:Optional[User] = await repo.get(user_id=user_id)
    if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='User not found')
    return UserRead.model_validate(user)

@router.get('' , response_model=list[UserRead] , status_code=status.HTTP_200_OK)
async def list_users( 
                     limit:int = Query(50 , ge=1  , le=200), 
                     offset:int = Query(0 , ge=0),
                     session:AsyncSession=Depends(get_session)):
    repo = UserRepository(session)
    users:list[User] = await repo.list(limit , offset)
    return users

@router.patch('/{user_id}' , response_model=UserRead , status_code=status.HTTP_200_OK)
async def update_user(
    user_id:Annotated[int , Path(ge=1)] , 
    payload:UserUpdate , 
    session:AsyncSession=Depends(get_session)): 
    repo = UserRepository(session)
    if payload.email :
        existing:Optional[User] = await repo.get_by_email(payload.email)
        if existing and existing.id != user_id :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail='Email is used by another user')
    user:Optional[User] = await repo.update(user_id , name=payload.name , email=payload.email)
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='User not found')
    return UserRead.model_validate(user)

@router.delete('/{user_id}' ,  status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id:Annotated[int , Path(ge=1)] , 
    session: AsyncSession = Depends(get_session)
):
    repo = UserRepository(session)
    ok:bool = await repo.delete(user_id)
    if not ok :
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    return None
