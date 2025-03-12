FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV SQLITE_DB="/var/lib/sqlite/sensor_data.db"
CMD ["python", "motion_sensor.py", "--offline"]