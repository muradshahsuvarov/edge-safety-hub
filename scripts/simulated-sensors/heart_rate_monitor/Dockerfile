# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy necessary files into the container
COPY . /app

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the heart rate monitor script
CMD ["python", "heart_rate_monitor.py"]