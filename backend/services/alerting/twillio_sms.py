from twilio.rest import Client

TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH = "your_twilio_auth_token"
TWILIO_PHONE = "+1234567890"

def send_sms_alert(message):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    client.messages.create(body=message, from_=TWILIO_PHONE, to="+recipient_number")
