from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from typing import Optional
from ..models import User, UserRole
from ..dependencies import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

@router.get("/")
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [
        {
            "id": u.id,
            "display_id": f"USR-{str(u.id).zfill(3)}",
            "name": u.username,
            "role": u.role.value if hasattr(u.role, 'value') else u.role,
            "status": "Active"
        }
        for u in users
    ]

@router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if username already exists
    result = await db.execute(select(User).where(User.username == user.username))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Username sudah digunakan")
    
    hashed_pw = pwd_context.hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pw, role=user.role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"status": "success", "message": "User berhasil dibuat", "id": new_user.id}

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    
    if user.username is not None:
        # Check if the new username is taken by another user
        result = await db.execute(select(User).where(User.username == user.username, User.id != user_id))
        existing = result.scalars().first()
        if existing:
            raise HTTPException(status_code=400, detail="Username sudah digunakan")
        db_user.username = user.username
    
    if user.password is not None and user.password.strip():
        db_user.hashed_password = pwd_context.hash(user.password)
    
    if user.role is not None:
        db_user.role = user.role
    
    await db.commit()
    return {"status": "success", "message": "User berhasil diperbarui"}

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    
    await db.delete(db_user)
    await db.commit()
    return {"status": "success", "message": "User berhasil dihapus"}
