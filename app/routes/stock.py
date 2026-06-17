import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import StockEntry, Depot
from ..schemas import StockEntryCreate, StockEntryRead
from ..dependencies import get_db

from pydantic import BaseModel

router = APIRouter()

class DepotCreate(BaseModel):
    name: str
    location: str

@router.post("/depots")
async def create_depot(depot: DepotCreate, db: AsyncSession = Depends(get_db)):
    new_depot = Depot(name=depot.name, location=depot.location)
    db.add(new_depot)
    await db.commit()
    return {"status": "success", "message": "Depot created"}

@router.get("/depots")
async def get_depots(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Depot))
    return result.scalars().all()

@router.post("/", response_model=StockEntryRead, status_code=status.HTTP_201_CREATED)
async def create_stock(entry: StockEntryCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        depot = await db.get(Depot, entry.depot_id)
        if not depot:
            raise HTTPException(status_code=404, detail="Depot not found")
        new_entry = StockEntry(**entry.dict())
        db.add(new_entry)
        await db.flush()
        await db.refresh(new_entry)
        return new_entry

@router.get("/depot/{depot_id}", response_model=list[StockEntryRead])
async def get_stock_by_depot(depot_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StockEntry).where(StockEntry.depot_id == depot_id))
    entries = result.scalars().all()
    return entries
