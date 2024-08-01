import random
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

# Define the data model for sensor data with an id
class SensorData(BaseModel):
    id: str
    CO2: float
    Temp: float
    Humi: float
    EC: float
    Pressure: float
    Flowmeters: float
    pH: float
    WaterlevelSensor1: float
    WaterlevelSensor2: float

# Define the data model for motor data with an id
class MotorData(BaseModel):
    id: str
    motor1: float
    motor2: float
    motor3: float

# In-memory stores for sensor and motor data
sensor_data_store: List[SensorData] = []
motor_data_store: List[MotorData] = []

# Helper function to generate random sensor data
def generate_random_sensor_data() -> SensorData:
    return SensorData(
        id=str(uuid4()),  # Generate a unique ID
        CO2=random.uniform(300, 800),  # Random CO2 level
        Temp=random.uniform(15, 35),   # Random temperature in Celsius
        Humi=random.uniform(20, 100),  # Random humidity percentage
        EC=random.uniform(0.5, 2.5),   # Random EC value
        Pressure=random.uniform(950, 1050),  # Random atmospheric pressure in hPa
        Flowmeters=random.uniform(0, 100),  # Random flowmeter reading
        pH=random.uniform(6.5, 8.5),  # Random pH value
        WaterlevelSensor1=random.uniform(0, 100),  # Random water level 1
        WaterlevelSensor2=random.uniform(0, 100)   # Random water level 2
    )

# Helper function to generate random motor data
def generate_random_motor_data() -> MotorData:
    return MotorData(
        id=str(uuid4()),  # Generate a unique ID
        motor1=random.randint(0, 1),  # Random motor state
        motor2=random.randint(0, 1),  # Random motor state
        motor3=random.randint(0, 1)   # Random motor state
    )

# POST endpoint to generate and add random sensor data
@app.post("/data/sensor/random/{count}")
async def add_random_sensor_data(count: int):
    for _ in range(count):
        random_data = generate_random_sensor_data()
        sensor_data_store.append(random_data)
    return {"message": f"Added {count} random sensor data entries successfully"}

# POST endpoint to generate and add random motor data
@app.post("/data/motor/random/{count}")
async def add_random_motor_data(count: int):
    for _ in range(count):
        random_data = generate_random_motor_data()
        motor_data_store.append(random_data)
    return {"message": f"Added {count} random motor data entries successfully"}

# GET endpoint to retrieve all sensor data
@app.get("/data/sensor/all")
async def get_all_sensor_data():
    if not sensor_data_store:
        return {"message": "No sensor data available"}

    # Convert all sensor data to a list of dictionaries
    all_sensor_data = [
        {
            "id": data.id,
            "CO2": round(data.CO2, 2),
            "Temp": round(data.Temp, 2),
            "Humi": round(data.Humi, 2),
            "EC": round(data.EC, 2),
            "Pressure": round(data.Pressure, 2),
            "Flowmeters": round(data.Flowmeters, 2),
            "pH": round(data.pH, 2),
            "WaterlevelSensor1": round(data.WaterlevelSensor1, 2),
            "WaterlevelSensor2": round(data.WaterlevelSensor2, 2),
        }
        for data in sensor_data_store
    ]
    
    return {"data": all_sensor_data}

# GET endpoint to retrieve all motor data
@app.get("/data/motor/all")
async def get_all_motor_data():
    if not motor_data_store:
        return {"message": "No motor data available"}

    # Convert all motor data to a list of dictionaries
    all_motor_data = [
        {
            "id": data.id,
            "motor1": data.motor1,
            "motor2": data.motor2,
            "motor3": data.motor3,
        }
        for data in motor_data_store
    ]
    
    return {"data": all_motor_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
