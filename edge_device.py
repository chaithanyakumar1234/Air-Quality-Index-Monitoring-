import requests
import random
import time

# Edge device parameters to simulate sensor readings
def collect_sensor_data():
    # Simulate sensor data collection
    data = {
        'PM2.5': random.uniform(0, 200),
        'PM10': random.uniform(0, 150),
        'NO2': random.uniform(0, 100),
        'SO2': random.uniform(0, 50),
        'CO': random.uniform(0, 10),
        'O3': random.uniform(0, 100),
    }
    return data

def send_data_to_fog(data):
    try:
        # Send data to fog layer
        response = requests.post("http://localhost:5000/edge_data", json=data)
        print("Data sent to fog layer:", data)
        print("Fog response:", response.json())
    except Exception as e:
        print("Error sending data to fog:", e)

# Continuously collect and send data to the fog layer
while True:
    data = collect_sensor_data()
    send_data_to_fog(data)
    time.sleep(5)  # Send data every 5 seconds
