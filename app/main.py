from fastapi import FastAPI, WebSocket, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from app.scheduler import notification_cron_job
import os
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup background tasks
    task = asyncio.create_task(notification_cron_job())
    yield
    # Cleanup on shutdown
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="FuelTrack Analytics", lifespan=lifespan)

# Database setup (SQLite async for local dev)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./fueltrack.db"
)
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include routers
from app.routes import stock, distribution, forecast, alerts, tracking, analytics, notifications, users, auth

app.include_router(stock.router, prefix="/api/stock", tags=["Stock"])
app.include_router(distribution.router, prefix="/api/distribution", tags=["Distribution"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["Forecast"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(tracking.router, prefix="/api/tracking", tags=["Tracking"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

# Pages routes
from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/login")

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# WebSocket for real‑time updates
@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_text("ping")
            await asyncio.sleep(5)
    except Exception:
        await websocket.close()
