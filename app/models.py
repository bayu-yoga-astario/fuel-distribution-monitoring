from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class UserRole(str, enum.Enum):
    OPERATOR = "operator"
    SUPERVISOR = "supervisor"
    MANAGER = "manager"

class FuelType(str, enum.Enum):
    PERTALITE = "Pertalite"
    PERTAMAX = "Pertamax"
    PERTAMAX_TURBO = "Pertamax Turbo"
    SOLAR = "Solar"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.OPERATOR)
    avatar_url = Column(String, nullable=True)

class Depot(Base):
    __tablename__ = "depots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=True)
    stock_entries = relationship("StockEntry", back_populates="depot")

class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=True)
    distribution_logs = relationship("DistributionLog", back_populates="station")

class StockEntry(Base):
    __tablename__ = "stock_entries"
    id = Column(Integer, primary_key=True, index=True)
    depot_id = Column(Integer, ForeignKey("depots.id"), nullable=False)
    fuel_type = Column(Enum(FuelType), nullable=False)
    quantity = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    depot = relationship("Depot", back_populates="stock_entries")

class DistributionLog(Base):
    __tablename__ = "distribution_logs"
    id = Column(Integer, primary_key=True, index=True)
    depot_id = Column(Integer, ForeignKey("depots.id"), nullable=False)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    fuel_type = Column(Enum(FuelType), nullable=False)
    quantity = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    depot = relationship("Depot")
    station = relationship("Station", back_populates="distribution_logs")

class Tanker(Base):
    __tablename__ = "tankers"
    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, nullable=False)
    capacity = Column(Float, nullable=False)
    status = Column(String, default="Idle")
    locations = relationship("TankerLocation", back_populates="tanker")

class TankerLocation(Base):
    __tablename__ = "tanker_locations"
    id = Column(Integer, primary_key=True, index=True)
    tanker_id = Column(Integer, ForeignKey("tankers.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tanker = relationship("Tanker", back_populates="locations")
