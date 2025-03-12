import sqlite3
import time
import smtplib
import json
import os
from email.mime.text import MIMEText
from twilio.rest import Client
from iridium_api import send_iridium_message  # ✅ Now uses the virtual port simulation

# SQLite Configuration
SQLITE_DB = os.getenv("SQLITE_DB", "/var/lib/sqlite/sensor_data.db")

# Alerting Thresholds
GAS_THRESHOLD = 50
HEART_RATE_THRESHOLD = 120

# Email Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = os.getenv("SMTP_PORT", 587)
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "your_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_email_password")
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "recipient_email@gmail.com")

# Twilio SMS Configuration (Optional)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_twilio_sid")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_twilio_token")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")
ALERT_PHONE_NUMBER = os.getenv("ALERT_PHONE_NUMBER", "+9876543210")

def send_email_alert(subject, message):
    """Send an email alert using SMTP."""
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_USERNAME
        msg["To"] = ALERT_EMAIL

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USERNAME, ALERT_EMAIL, msg.as_string())
        server.quit()
        print(f"📧 Email alert sent: {subject}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_sms_alert(message):
    """Send an SMS alert using Twilio."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=ALERT_PHONE_NUMBER
        )
        print(f"📱 SMS alert sent: {message}")
    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")

def check_alerts():
    """Monitor SQLite and trigger alerts."""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            sensor_type TEXT NOT NULL,
            value TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    last_checked_id = 0

    while True:
        cursor.execute("SELECT id, device_id, sensor_type, value, timestamp FROM sensor_data WHERE id > ?", (last_checked_id,))
        rows = cursor.fetchall()

        for row in rows:
            record_id, device_id, sensor_type, value, timestamp = row
            value_data = json.loads(value)

            alert_triggered = False
            alert_message = f"⚠️ Alert from {device_id} at {timestamp}:\n"

            if sensor_type == "gas_detector" and value_data.get("gas_level", 0) > GAS_THRESHOLD:
                alert_triggered = True
                alert_message += f"🔥 High Gas Level: {value_data['gas_level']} ppm\n"

            if sensor_type == "heart_rate_monitor" and value_data.get("heart_rate", 0) > HEART_RATE_THRESHOLD:
                alert_triggered = True
                alert_message += f"💓 High Heart Rate: {value_data['heart_rate']} bpm\n"

            if alert_triggered:
                send_email_alert("Emergency Alert 🚨", alert_message)
                send_sms_alert(alert_message)
                send_iridium_message(alert_message)  # ✅ Now simulates sending Iridium messages

            last_checked_id = record_id

        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    print("🔍 Alerting Service Running...")
    check_alerts()