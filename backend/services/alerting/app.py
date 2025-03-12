from fastapi import FastAPI
from twilio_sms import send_sms_alert
from email_alerts import send_email_alert

app = FastAPI()

@app.post("/alert")
async def trigger_alert(alert_message: str):
    send_sms_alert(alert_message)
    send_email_alert(alert_message)
    return {"message": "Alert sent successfully"}
