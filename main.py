from fastapi import FastAPI
import json
import pandas as pd
import os

# File names
ACCELEROMETER_FILE = "GY-91.csv"
TEMPERATURE_HUMIDITY_FILE = "HDC-1080.csv"
LATITUDE_LONGITUDE_FILE = "NEO-6M.csv"
OCTA_FILE = "OctaCSV.csv"

# Build the full paths to the files using os.path
CSV_ACCELEROMETER_PATH = os.path.join("data", ACCELEROMETER_FILE)
CSV_TEMPERATURE_HUMIDITY_PATH = os.path.join("data", TEMPERATURE_HUMIDITY_FILE)
CSV_LATITUDE_LONGITUDE_PATH = os.path.join("data", LATITUDE_LONGITUDE_FILE)
CSV_OCTA_PATH = os.path.join("data", OCTA_FILE)


# Read CSV files and handle FileNotFoundError
def read_csv_file(csv_path):
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        return None
    

app = FastAPI()

# Main
@app.get("/")
def index():
    return {"message": "Octa-API"}

# GY-91
@app.get("/accelerometer")
def accelerometer():
    df = read_csv_file(CSV_ACCELEROMETER_PATH)
    if df is None:
        return []
    
    # Convert the data into a structured JSON format
    json_data = []
    for index, row in df.iterrows():
        accelerometer_values = row["Acelerometer"].strip("[]").split(", ")
        gyroscope_values = row["Gyroscope"].strip("[]").split(", ")
        magnetometer_values = row["Magnetometer"].strip("[]").split(", ")
        
        x_accelerometer, y_accelerometer, z_accelerometer = map(float, accelerometer_values)
        formatted_accelerometer = {
            "x": x_accelerometer,
            "y": y_accelerometer,
            "z": z_accelerometer
        }
        
        x_gyroscope, y_gyroscope, z_gyroscope = map(float, gyroscope_values)
        formatted_gyroscope = {
            "x": x_gyroscope,
            "y": y_gyroscope,
            "z": z_gyroscope
        }
        
        x_magnetometer, y_magnetometer, z_magnetometer = map(float, magnetometer_values)
        formatted_magnetometer = {
            "x": x_magnetometer,
            "y": y_magnetometer,
            "z": z_magnetometer
        }
        
        entry = {
            "Time": row["Time"],
            "Acelerometer": formatted_accelerometer,
            "Gyroscope": formatted_gyroscope,
            "Magnetometer": formatted_magnetometer
        }
        
        json_data.append(entry)
    
    # Return the JSON as a response
    return json_data

# HDC-1080
@app.get("/temperatureHumidity")
def temperature_humidity():
    df = read_csv_file(CSV_TEMPERATURE_HUMIDITY_PATH)
    if df is None:
        return []
    
    # Convert the data into a structured JSON format
    json_data = []
    for index, row in df.iterrows():
        entry = {
            "Time": row["Time"],
            "Temperature": row["Temperature(C)"],
            "Humidity": row["Humidity"]
        }
        json_data.append(entry)
    
    # Return the JSON as a response
    return json_data

# NEO-6M
@app.get("/latitudeLongitude")
def latitude_longitude():
    df = read_csv_file(CSV_LATITUDE_LONGITUDE_PATH)
    if df is None:
        return []
    
    json_data = df.to_json(orient="records", date_format="iso", indent=2)
    return json.loads(json_data)

# OctaCSV
@app.get("/octa")
def octa():
    df = read_csv_file(CSV_OCTA_PATH)
    if df is None:
        return []
    
    json_data = df.to_json(orient="records", date_format="iso", indent=2)
    return json.loads(json_data)