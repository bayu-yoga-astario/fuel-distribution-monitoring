from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .models import FuelType

class StockEntryCreate(BaseModel):
    depot_id: int = Field(..., description="ID of the depot providing the fuel")
    fuel_type: FuelType = Field(..., description="Type of fuel, e.g., 'Pertamax', 'Solar'")
    quantity: float = Field(..., gt=0, description="Quantity in liters")
    timestamp: Optional[datetime] = None

class StockEntryRead(BaseModel):
    id: int
    depot_id: int
    fuel_type: FuelType
    quantity: float
    timestamp: datetime

    class Config:
        orm_mode = True

class DistributionCreate(BaseModel):
    depot_id: int
    station_id: int
    fuel_type: FuelType
    quantity: float = Field(..., gt=0)
    timestamp: Optional[datetime] = None

class DistributionRead(BaseModel):
    id: int
    depot_id: int
    station_id: int
    fuel_type: FuelType
    quantity: float
    timestamp: datetime

    class Config:
        orm_mode = True

class ForecastRead(BaseModel):
    fuel_type: FuelType
    predicted_quantity: float
    date: datetime

    class Config:
        orm_mode = True
