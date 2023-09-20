from fastapi import FastAPI
import pandas as pd
import os
import numpy as np

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
    if df is None or df.empty:
        return {}
    
    #última fila del DataFrame
    last_row = df.iloc[-1]
    
    json_data = []
    #formatear datos de la ultima fila
    accelerometer_values = last_row["Acelerometer"].strip("[]").split(", ")
    gyroscope_values = last_row["Gyroscope"].strip("[]").split(", ")
    magnetometer_values = last_row["Magnetometer"].strip("[]").split(", ")
    
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
        "Time": last_row["Time"],
        "Acelerometer": formatted_accelerometer,
        "Gyroscope": formatted_gyroscope,
        "Magnetometer": formatted_magnetometer
    }
    
    json_data.append(entry)
    
    return entry


# HDC-1080
@app.get("/temperatureHumidity")
def temperature_humidity():
    df = read_csv_file(CSV_TEMPERATURE_HUMIDITY_PATH)
    if df is None or df.empty:
        return {}

    # Get the last row of the DataFrame
    last_row = df.iloc[-1]

    # Convert the last row into a dictionary
    last_row_dict = {
        "Time": last_row["Time"],
        "Temperature": last_row["Temperature(C)"],
        "Humidity": last_row["Humidity"]
    }

    # Return the last row as a JSON response
    return last_row_dict

# NEO-6M
@app.get("/latitudeLongitude")
def latitude_longitude():
    df = read_csv_file(CSV_LATITUDE_LONGITUDE_PATH)
    if df is None or df.empty:
        return {}

    # Get the last row of the DataFrame
    last_row = df.iloc[-1]

    # Convert the last row into a dictionary
    last_row_dict = {
        "Time": last_row["Time"],
        "Latitude": last_row["Latitude"],
        "Longitude": last_row["Longitude"]
    }

    # Return the last row as a JSON response
    return last_row_dict


# OctaCSV
@app.get("/octa")
def octa():
    df = read_csv_file(CSV_OCTA_PATH)
    if df is None or df.empty:
        return {}

    # Get the last row of the DataFrame
    last_row = df.iloc[-1]

    # Convert the last row into a dictionary
    last_row_dict = {
        "hdc_temperature": last_row["hdc_temperature"],
        "bmp_temperature": last_row["bmp_temperature"],
        "humidity": last_row["humidity"],
        "pressure": last_row["pressure"],
        "altitude": last_row["altitude"],
        "time": last_row["time"]
    }

    return last_row_dict


#accelerometerTotalSum
@app.get("/accelerometerTotalSum")
def accelerometer_total_sum():
    df = read_csv_file(CSV_ACCELEROMETER_PATH)
    if df is None or df.empty:
        return {}

    # Get the last row of the DataFrame
    last_row = df.iloc[-1]
    accelerometer_values = last_row["Acelerometer"].strip("[]").split(", ")
    x_accelerometer, y_accelerometer, z_accelerometer = map(float, accelerometer_values)
    # Calculate the sum of the x, y, and z components of the accelerometer
    total_sum = x_accelerometer + y_accelerometer + z_accelerometer
    
    response_data = {
        "TotalSum": total_sum
    }
    return response_data


#orientation
@app.get("/orientation")
def get_orientation_from_csv():
    df = pd.read_csv(CSV_ACCELEROMETER_PATH)
    if df.empty:
        return {}

    last_row = df.iloc[-1]
    mag_data_str = last_row["Magnetometer"]
    mag_data = eval(mag_data_str)

    angle = np.arctan2(mag_data[1], mag_data[0])

    # Convert the angle to degrees.
    angle_deg = (angle * 180) / np.pi

    return {"angle_deg": angle_deg}





