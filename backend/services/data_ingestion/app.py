from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import mqtt_client
import models

# Initialize FastAPI app
app = FastAPI()

# Ensure database tables are created
models.Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Model for incoming sensor data
class SensorData(BaseModel):
    device_id: str
    sensor_type: str  # "gas", "motion", "heart_rate"
    value: float
    timestamp: str

@app.post("/ingest")
async def ingest_sensor_data(data: SensorData, db: Session = Depends(get_db)):
    new_entry = models.SensorData(
        device_id=data.device_id,
        sensor_type=data.sensor_type,
        value=data.value,
        timestamp=data.timestamp
    )
    db.add(new_entry)
    db.commit()
    return {"message": "Data stored successfully"}
