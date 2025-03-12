# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# ✅ Install system dependencies (including gcc)
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy only requirements.txt first (ensures efficient caching)
COPY services/alerting-service/requirements.txt /app/

# ✅ Install dependencies before copying other files
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Now copy the rest of the application
COPY services/alerting-service/ /app/

# Set environment variables
ENV SQLITE_DB="/var/lib/sqlite/sensor_data.db"
ENV SMTP_SERVER="smtp.gmail.com"
ENV SMTP_PORT=587
ENV EMAIL_USERNAME="your_email@gmail.com"
ENV EMAIL_PASSWORD="your_email_password"
ENV ALERT_EMAIL="recipient_email@gmail.com"
ENV TWILIO_ACCOUNT_SID="your_twilio_sid"
ENV TWILIO_AUTH_TOKEN="your_twilio_token"
ENV TWILIO_PHONE_NUMBER="+1234567890"
ENV ALERT_PHONE_NUMBER="+9876543210"

# Run the alerting service
CMD ["python", "alerting_service.py"]