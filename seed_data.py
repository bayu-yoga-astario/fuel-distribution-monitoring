import asyncio
from datetime import datetime, timedelta
import random
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Depot, Station, StockEntry, DistributionLog, FuelType, Tanker, TankerLocation
from app.main import DATABASE_URL

async def seed():
    engine = create_async_engine(DATABASE_URL, echo=False)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        # Seed Depots
        d1 = Depot(name="Plumpang", location="Jakarta")
        d2 = Depot(name="Tanjung Gerem", location="Banten")
        session.add_all([d1, d2])
        await session.flush()

        # Seed Stations
        s1 = Station(name="SPBU 31.102.02", location="Sudirman")
        s2 = Station(name="SPBU 34.114.05", location="Kemang")
        session.add_all([s1, s2])
        await session.flush()

        # Seed Tankers
        t1 = Tanker(license_plate="B 1234 XYZ", capacity=24000)
        t2 = Tanker(license_plate="B 5678 ABC", capacity=16000)
        session.add_all([t1, t2])
        await session.flush()

        # Seed 3 months of historical Distribution logs
        now = datetime.utcnow()
        fuel_types = list(FuelType)
        logs = []
        for i in range(300):
            past_date = now - timedelta(days=random.randint(1, 90), hours=random.randint(1, 24))
            logs.append(
                DistributionLog(
                    depot_id=random.choice([d1.id, d2.id]),
                    station_id=random.choice([s1.id, s2.id]),
                    fuel_type=random.choice(fuel_types),
                    quantity=random.randint(8000, 24000),
                    timestamp=past_date
                )
            )
            logs.append(
                StockEntry(
                    depot_id=random.choice([d1.id, d2.id]),
                    fuel_type=random.choice(fuel_types),
                    quantity=random.randint(50000, 200000),
                    timestamp=past_date
                )
            )
        
        session.add_all(logs)
        await session.commit()
        print("Database seeded with 3 months of mock historical data!")

if __name__ == "__main__":
    asyncio.run(seed())
