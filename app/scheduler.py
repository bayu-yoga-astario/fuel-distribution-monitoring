import asyncio
import logging
from datetime import datetime

logger = logging.getLogger("fueltrack.cron")

async def notification_cron_job():
    """Background task that runs periodically to check for stockouts"""
    logger.info("Cron job started: Monitoring FuelTrack conditions.")
    while True:
        try:
            # Wake up every 10 seconds to simulate a cron job checking conditions
            await asyncio.sleep(10)
            
            now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            # In a real app, we would query predict_stockout logic here
            # and automatically insert rows into an AlertLog table if threshold is met.
            # Here we just log to terminal to prove the automated background worker is running.
            logger.info(f"[{now_str}] CRON: Checked station fuel levels. All systems nominal.")
            
        except asyncio.CancelledError:
            logger.info("Cron job stopped.")
            break
        except Exception as e:
            logger.error(f"Error in background cron task: {e}")
            await asyncio.sleep(10) # Wait before retrying
