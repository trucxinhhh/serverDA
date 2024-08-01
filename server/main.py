import random
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data model for sensor data
class SensorData(BaseModel):
    CO2: float
    Temp: float
    Humi: float
    EC: float
    Pressure: float
    Flowmeters: float
    pH: float
    WaterlevelSensor1: float
    WaterlevelSensor2: float

# Define the data model for motor data
class MotorData(BaseModel):
    motor1: float
    motor2: float
    motor3: float

# Combine the data models for sensor and motor data
class DataModel(BaseModel):
    id: int
    sensor_data: SensorData
    motor_data: MotorData

# In-memory store for the data
data_store: List[DataModel] = []
next_id = 1

# Helper function to generate random data
def generate_random_data() -> DataModel:
    global next_id
    data = DataModel(
        id=next_id,
        sensor_data=SensorData(
            CO2=random.uniform(300, 800),  # Random CO2 level
            Temp=random.uniform(15, 35),   # Random temperature in Celsius
            Humi=random.uniform(20, 100),  # Random humidity percentage
            EC=random.uniform(0.5, 2.5),   # Random EC value
            Pressure=random.uniform(950, 1050),  # Random atmospheric pressure in hPa
            Flowmeters=random.uniform(0, 100),  # Random flowmeter reading
            pH=random.uniform(6.5, 8.5),  # Random pH value
            WaterlevelSensor1=random.uniform(0, 100),  # Random water level 1
            WaterlevelSensor2=random.uniform(0, 100)   # Random water level 2
        ),
        motor_data=MotorData(
            motor1=random.randint(0, 1),  # Random motor state
            motor2=random.randint(0, 1),  # Random motor state
            motor3=random.randint(0, 1)   # Random motor state
        )
    )
    next_id += 1
    return data

# POST endpoint to generate and add random data
@app.post("/data/random/{count}")
async def add_random_data(count: int):
    for _ in range(count):
        random_data = generate_random_data()
        data_store.append(random_data)
    return {"message": f"Added {count} random data entries successfully"}

# GET endpoint to retrieve the latest data
@app.get("/data/latest")
async def get_latest_data():
    if not data_store:
        return {"message": "No data available"}
    
    latest_data = data_store[-1]
    return {
        "id": latest_data.id,
        "CO2": latest_data.sensor_data.CO2,
        "Temp": round(latest_data.sensor_data.Temp, 2),
        "Humi": round(latest_data.sensor_data.Humi, 2),
        "EC": round(latest_data.sensor_data.EC, 2),
        "Pressure": round(latest_data.sensor_data.Pressure,2),
        "Flowmeters": round(latest_data.sensor_data.Flowmeters,2),
        "pH": round(latest_data.sensor_data.pH,2),
        "WaterlevelSensor1": round(latest_data.sensor_data.WaterlevelSensor1,2),
        "WaterlevelSensor2": round(latest_data.sensor_data.WaterlevelSensor2,2),
        "motor1": latest_data.motor_data.motor1,
        "motor2": latest_data.motor_data.motor2,
        "motor3": latest_data.motor_data.motor3,
    }

# GET endpoint to retrieve all data
@app.get("/data/all")
async def get_all_data():
    if not data_store:
        return {"message": "No data available"}

    # Convert all data to a list of dictionaries
    all_data = [
        {
            "id": data.id,
            "CO2": round(data.sensor_data.CO2,2),
            "Temp": round(data.sensor_data.Temp, 2),
            "Humi": round(data.sensor_data.Humi, 2),
            "EC": round(data.sensor_data.EC, 2),
            "Pressure": round(data.sensor_data.Pressure,2),
            "Flowmeters": round(data.sensor_data.Flowmeters,2),
            "pH": round(data.sensor_data.pH,2),
            "WaterlevelSensor1": round(data.sensor_data.WaterlevelSensor1,2),
            "WaterlevelSensor2": round(data.sensor_data.WaterlevelSensor2,2),
            "motor1": data.motor_data.motor1,
            "motor2": data.motor_data.motor2,
            "motor3": data.motor_data.motor3,
        }
        for data in data_store
    ]
    
    return {"data": all_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
