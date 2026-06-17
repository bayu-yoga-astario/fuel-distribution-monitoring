from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import TankerLocation, Tanker
from ..dependencies import get_db

router = APIRouter()

class GPSLocation(BaseModel):
    tanker_id: int
    latitude: float
    longitude: float
    speed: float

@router.post("/location")
async def update_location(location: GPSLocation, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        new_loc = TankerLocation(
            tanker_id=location.tanker_id,
            latitude=location.latitude,
            longitude=location.longitude,
            speed=location.speed,
            timestamp=datetime.utcnow()
        )
        db.add(new_loc)
        await db.commit()
    return {"status": "success"}

@router.get("/active-fleet")
async def get_active_fleet(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tanker))
    tankers = result.scalars().all()
    
    fleet = []
    if not tankers:
        # Provide rich mock data if database is empty for demo purposes
        return [
            {"truck_id": "B 9012 XY", "lat": -6.1264, "lng": 106.8993, "speed": 60, "status": "Moving"},
            {"truck_id": "B 1143 ZA", "lat": -5.9272, "lng": 105.9980, "speed": 0, "status": "Unloading"},
            {"truck_id": "B 8821 CX", "lat": -6.2000, "lng": 106.8166, "speed": 45, "status": "Moving"},
            {"truck_id": "B 7710 DF", "lat": -6.4014, "lng": 107.4526, "speed": 0, "status": "Idle"}
        ]
        
    for t in tankers:
        fleet.append({
            "truck_id": t.license_plate,
            "lat": -6.15 + (t.id * 0.01),
            "lng": 106.90 + (t.id * 0.01),
            "speed": 60 if t.id % 2 == 0 else 0,
            "status": "Moving" if t.id % 2 == 0 else "Unloading"
        })
    return fleet
