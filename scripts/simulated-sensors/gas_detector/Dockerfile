# 🚀 Use an official lightweight Python image
FROM python:3.9-slim

# 📂 Set the working directory inside the container
WORKDIR /app

# 🛠 Copy necessary files into the container
COPY . /app

# 📦 Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 📌 Set environment variables (if needed)
ENV SQLITE_DB="/var/lib/sqlite/sensor_data.db"

# 🏃 Set the command to run the script
CMD ["python", "gas_detector.py", "--offline"]