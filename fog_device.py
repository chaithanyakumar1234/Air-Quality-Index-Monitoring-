from flask import Flask, jsonify, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained AQI model
rf_model = joblib.load('random_forest_aqi_model.pkl')

# Data buffer to hold edge device data
data_buffer = []


# Serve the main webpage
@app.route('/')
def index():
    return render_template('index.html')  # This serves index.html

# Endpoint to receive data from edge devices
@app.route('/edge_data', methods=['POST'])
def receive_edge_data():
    global data_buffer
    data = request.json
    data_buffer.append(data)
    
    # Process data when buffer has enough data points
    if len(data_buffer) >= 5:
        avg_data = pd.DataFrame(data_buffer).mean().to_dict()
        aqi_alert = check_aqi(avg_data)
        data_buffer = []  # Clear buffer after processing
        return jsonify(aqi_alert)
    return jsonify({'status': 'OK', 'message': 'Data received at fog layer'})

# Endpoint for the web interface to check the latest AQI status
@app.route('/check_aqi', methods=['GET'])
def check_aqi_web():
    # Check AQI based on last average data if available
    if data_buffer:
        avg_data = pd.DataFrame(data_buffer).mean().to_dict()
        aqi_alert = check_aqi(avg_data)
    else:
        aqi_alert = {'status': 'OK', 'message': 'No data received yet from edge devices.'}
    return jsonify(aqi_alert)

# Process data and apply the AQI model
def check_aqi(sensor_data):
    # Convert data into DataFrame for model prediction
    df = pd.DataFrame([sensor_data])
    aqi_prediction = rf_model.predict(df)[0]

    # Determine alert level based on prediction
    if aqi_prediction > 100:
        alert = {
            'status': 'ALERT',
            'message': f'High AQI detected: {aqi_prediction:.2f}. Stay indoors.',
        }
    else:
        alert = {
            'status': 'SAFE',
            'message': f'Air quality is safe: {aqi_prediction:.2f}.',
        }
    return alert

# Run the fog server
if __name__ == '__main__':
    app.run(debug=True)
