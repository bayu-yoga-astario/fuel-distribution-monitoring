from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class TwilioConfig(BaseModel):
    api_key: str

class SMTPConfig(BaseModel):
    smtp_server: str
    port: int

@router.post("/config/whatsapp")
async def config_whatsapp(config: TwilioConfig):
    return {"status": "success", "message": "WhatsApp API Key saved"}

@router.post("/config/email")
async def config_email(config: SMTPConfig):
    return {"status": "success", "message": "SMTP Server saved"}

@router.post("/trigger-alert")
async def trigger_alert(channel: str, recipient: str, message: str):
    # Dummy logic to simulate sending message
    return {"status": "success", "channel": channel, "delivered_to": recipient}
