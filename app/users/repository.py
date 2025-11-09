from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.users.models import User


class UserRepository :
    def __init__(self , session:AsyncSession):
        self.session = session
    
    async def create(self , * , name:str , email:str , password:str)->User:
        user = User(name=name , email=email , password_hash=hash_password(password))
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        await self.session.commit()
        return user
    
    async def get(self , user_id:int)->Optional[User]:
        res = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return res.scalar_one_or_none()
    
    async def get_by_email(self , email:str)->Optional[User]:
        stmt = select(User).where(User.email == email.lower().strip())
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
    
    async def list(self , limit:int=50 , offset:int = 0)->list[User]:
        stmt = select(User).limit(limit).offset(offset).order_by(User.id)
        res = await self.session.execute(stmt)
        users = list(res.scalars().all())
        return users
    
    async def update(self , id:int , * , name:Optional[str] , email:Optional[str]):
        res = await self.session.execute(
            select(User).where(User.id == id)
        )
        user :Optional[User] = res.scalar_one_or_none()
        if user is None : 
            return None
        if name is not None :
            user.name = name 
        if email is not None :
            user.email = email.lower().strip()
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(user)
        return user 
    
    async def delete(self , id:int)->bool:
        res = await self.session.execute(
            select(User).where(User.id == id)
        )
        user: Optional[User] = res.scalar_one_or_none()
        if user is None :
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True
    