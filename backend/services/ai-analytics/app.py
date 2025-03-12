from fastapi import FastAPI
import inference
from pydantic import BaseModel

app = FastAPI()

class SensorData(BaseModel):
    device_id: str
    sensor_type: str
    value: float
    timestamp: str

@app.post("/predict")
async def predict_hazard(data: SensorData):
    prediction = inference.analyze_data(data)
    return {"prediction": prediction}
