import asyncio

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.users.models import User


async def seed():
    async with AsyncSessionLocal() as session :
        u = User(name='selia' , email='selia@gmail.com' , password_hash=hash_password('password'))
        session.add(u)
        await session.commit()
        
if __name__ == '__main__' :
    asyncio.run(seed())