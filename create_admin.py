import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import DATABASE_URL
from app.models import User, UserRole
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed():
    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
    async with AsyncSessionLocal() as db:
        admin = User(username="admin", hashed_password=pwd_context.hash("admin123"), role=UserRole.MANAGER)
        db.add(admin)
        await db.commit()
        print("Admin user created!")

if __name__ == "__main__":
    asyncio.run(seed())
