from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.dependencies import get_db
from app.models import DistributionLog

router = APIRouter()

@router.get("/")
async def get_distribution_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DistributionLog)
        .options(selectinload(DistributionLog.depot), selectinload(DistributionLog.station))
        .order_by(DistributionLog.timestamp.desc())
        .limit(100)
    )
    logs = result.scalars().all()
    
    return [
        {
            "id": log.id,
            "depot_name": log.depot.name if log.depot else "Unknown Depot",
            "station_name": log.station.name if log.station else "Unknown Station",
            "fuel_type": log.fuel_type,
            "quantity": log.quantity,
            "timestamp": log.timestamp.isoformat()
        }
        for log in logs
    ]
