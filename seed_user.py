import sys
import os
sys.path.insert(0, os.getcwd())

import asyncio
from app.main import AsyncSessionLocal
from app.models import User, UserRole
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

async def seed():
    async with AsyncSessionLocal() as db:
        async with db.begin():
            # Check if admin already exists
            result = await db.execute(select(User).where(User.username == 'admin'))
            admin = result.scalars().first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@fueltrack.com',
                    hashed_password=pwd_context.hash('admin123'),
                    role=UserRole.ADMIN
                )
                db.add(admin)
                print('User admin seeded with password admin123!')
            else:
                print('Admin user already exists.')

asyncio.run(seed())
