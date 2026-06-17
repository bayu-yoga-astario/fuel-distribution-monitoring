import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.models import Base
from app.main import DATABASE_URL

async def init_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
