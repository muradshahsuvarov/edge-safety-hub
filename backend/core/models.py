from sqlalchemy import Column, Integer, String, Float, DateTime
from core.database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    sensor_type = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime)