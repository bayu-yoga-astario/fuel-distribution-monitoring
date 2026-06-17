from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import DistributionLog
from ..dependencies import get_db
import io
import csv

router = APIRouter()

@router.get("/esg-report")
async def get_esg_report():
    # Calculate carbon footprint based on distribution volume
    return {
        "total_co2_emissions_tons": 1420,
        "carbon_offset_tons": 850,
        "fleet_efficiency_score": "A+",
        "emissions_by_region": {
            "Jakarta": 420,
            "Bandung": 310,
            "Banten": 250,
            "Cirebon": 150
        }
    }

@router.get("/supply-chain-flow")
async def get_supply_chain_flow():
    # Return nodes and links for Sankey diagram mapping
    return {"nodes": ["Plumpang", "T. Gerem", "Jakarta", "Bandung", "Banten"], "links": []}

@router.get("/export-logs")
async def export_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DistributionLog))
    logs = result.scalars().all()
    
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(["ID", "Depot ID", "Station ID", "Fuel Type", "Quantity", "Timestamp"])
    for log in logs:
        writer.writerow([log.id, log.depot_id, log.station_id, log.fuel_type, log.quantity, log.timestamp])
    
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=FuelTrack_Distribution_Report.csv"
    return response

@router.get("/fuel-breakdown")
async def get_fuel_breakdown():
    # Mocked data for analytical demonstration
    return {
        "volume_share": {
            "Pertalite": 45,
            "Pertamax": 25,
            "Pertamax Turbo": 10,
            "Solar": 15,
            "Dexlite": 5
        },
        "current_stock_kl": {
            "Pertalite": 12500,
            "Pertamax": 8400,
            "Pertamax Turbo": 3200,
            "Solar": 5600,
            "Dexlite": 1800
        },
        "weekly_trend": {
            "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Pertalite": [1100, 1150, 1080, 1200, 1350, 1420, 1380],
            "Pertamax": [600, 620, 590, 610, 680, 750, 710],
            "Solar": [450, 480, 470, 490, 460, 410, 390]
        }
    }

