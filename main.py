from fastapi import FastAPI
import json
import pandas as pd

#routes
csv_accelerometer_path = "data\\GY-91.csv"
csv_temperatureHumidity_path = "data\\HDC-1080.csv"
csv_latitudeLongitude_path = "data\\NEO-6M.csv"
csv_octa_path ="data\\OctaCSV.csv"


app = FastAPI()

#main
@app.get("/")
def index():
    return {"message":"Octa-API"}

# GY-91
@app.get("/accelerometer")
def accelerometer():
    # Read the CSV file using pandas
    df = pd.read_csv(csv_accelerometer_path)
    
    # Convert the data into a structured JSON format
    json_data = df.to_json(orient="records", date_format="iso", indent=2)
    
    # Return the JSON as a response
    return json.loads(json_data)  # Convert the JSON into a Python object (dict/list) before returning


#HDC-1080
@app.get("/temperatureHumidity")
def accelerometer():
    df = pd.read_csv(csv_temperatureHumidity_path)
    json_data = df.to_json(orient="records", date_format="iso", indent=2)
    
    return json.loads(json_data)

#NEO-6M
@app.get("/latitudeLongitude")
def accelerometer():
    df = pd.read_csv(csv_latitudeLongitude_path)
    json_data = df.to_json(orient="records", date_format="iso", indent=2)
    
    return json.loads(json_data)

#OctaCSV
@app.get("/octa")
def accelerometer():
    df = pd.read_csv(csv_octa_path)
    json_data = df.to_json(orient="records", date_format="iso", indent=2)
    
    return json.loads(json_data)