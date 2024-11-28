import psutil
import requests
import time
import logging
import csv
import os
import shutil
import subprocess
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from datetime import datetime
from collections import deque

# APACHE_STATUS_URL = "http://172.28.191.215/server-status?auto"
APACHE_STATUS_URL = "http://localhost/server-status?auto"
ACCESS_LOG_FILE = "/var/log/apache2/access.log"

# Configure logging
logging.basicConfig(filename="monitoring.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Constants
WEATHER_API_KEY = "7a8fdd951ab780e11ad83ac773f07e7f"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
LOCATION = "Kitchener,CA"
CSV_FILE = "system_metrics.csv"

# Degradation Thresholds
CPU_THRESHOLD_UPPER = 90  # Trigger degradation
CPU_THRESHOLD_LOWER = 25  # Return to normal

MEMORY_THRESHOLD_UPPER = 90  # Trigger degradation
MEMORY_THRESHOLD_LOWER = 40  # Return to normal

# Cooldown Settings
COOLDOWN_PERIOD = 60  # seconds

# Paths to HTML files
CURRENT_HTML = "/var/www/html/index.html"
HIGH_LOAD_HTML = "/var/www/html/high_load.html"
NORMAL_CONTENT_HTML = "/var/www/html/normal_content.html"

# Flag to determine memory mode (True = total memory usage, False = actual memory usage)
USE_TOTAL_MEMORY = False

# Set timeouts for network requests
NETWORK_TIMEOUT = 5  # seconds

# Paths to the trained model and scaler
MODEL_PATH = 'isolation_forest_model.pkl'
SCALER_PATH = 'scaler.pkl'
ENCODER_PATH = 'encoder.pkl'  # Save the encoder during data preparation

try:
    # Load the Isolation Forest model
    model = joblib.load(MODEL_PATH)
    logging.info("Isolation Forest model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading Isolation Forest model: {e}")
    exit(1)

try:
    # Load the scaler and encoder
    scaler = joblib.load(SCALER_PATH)
    encoder = joblib.load('encoder.pkl')
    logging.info("Scaler and OneHotEncoder loaded successfully.")
except Exception as e:
    logging.error(f"Error loading scaler or encoder: {e}")
    exit(1)

# After loading the encoder
FEATURES = [
    'CPU Usage (%)',
    'Memory Usage (%)',
    'CPU Temp (°C)',
    'Weather Temp (°C)',
    'Humidity (%)',
    'ReqPerSec',
    'Average Latency (ms)',
] + list(encoder.get_feature_names_out(['Weather Description']))

# Function to fetch weather data
def fetch_weather():
    try:
        response = requests.get(WEATHER_API_URL, params={
            "q": LOCATION,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }, timeout=NETWORK_TIMEOUT)
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            weather = data['weather'][0]['description']
            return temp, humidity, weather
        else:
            logging.error(f"Weather API Error: {data.get('message', 'Unknown error')}")
            return None, None, None
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return None, None, None

# Function to calculate memory usage
def calculate_memory_usage():
    try:
        memory = psutil.virtual_memory()
        if USE_TOTAL_MEMORY:
            return memory.percent
        else:
            actual_memory_percent = 100 * (memory.used - memory.buffers - memory.cached) / memory.total
            return actual_memory_percent
    except Exception as e:
        logging.error(f"Error calculating memory usage: {e}")
        return 0  # Return 0 if unable to calculate

# Function to switch content based on system load
def switch_content(degrade=False):
    try:
        # Determine the target content
        # print(degrade)
        target_content_path = HIGH_LOAD_HTML if degrade else NORMAL_CONTENT_HTML

        # Read the contents of CURRENT_HTML
        with open(CURRENT_HTML, 'r') as current_file:
            current_content = current_file.read()

        # Read the contents of the target content
        with open(target_content_path, 'r') as target_file:
            target_content = target_file.read()

        # Check if the contents are the same
        if current_content == target_content:
            logging.info("Content already matches the target. No changes made.")
            print("[INFO] Content already matches the target. No changes made.")
            return

        # Switch the content by copying the target file to CURRENT_HTML
        shutil.copyfile(target_content_path, CURRENT_HTML)
        # os.utime(CURRENT_HTML, None)
        # subprocess.run(["curl", "http://localhost"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.info(f"Content switched to {'high_load.html' if degrade else 'normal_content.html'}")
        print(f"[INFO] Content switched to {'high_load.html' if degrade else 'normal_content.html'}")
    except Exception as e:
        logging.error(f"Error switching content: {e}")
        print(f"[ERROR] Error switching content: {e}")

# Function to fetch Apache metrics
def fetch_apache_metrics():
    try:
        response = requests.get(APACHE_STATUS_URL, timeout=NETWORK_TIMEOUT)
        if response.status_code == 200:
            data = response.text
            metrics = {}
            for line in data.splitlines():
                if ": " in line:
                    key, value = line.split(": ", 1)
                    metrics[key.strip()] = value.strip()
            return metrics
        else:
            logging.error(f"Failed to fetch Apache metrics: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error fetching Apache metrics: {e}")
        return None

# Function to fetch latency from access logs
# Function to fetch average latency from the last n valid lines in access logs
def get_average_latency(n=100):
    try:
        lines_to_read = n
        block_size = 8192  # Adjust block size as needed
        data = bytearray()
        lines = []
        latencies = []

        with open(ACCESS_LOG_FILE, 'rb') as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            remaining_size = file_size

            while len(lines) < lines_to_read and remaining_size > 0:
                # Determine how much to read
                read_size = min(block_size, remaining_size)
                # Move the cursor back
                f.seek(remaining_size - read_size)
                # Read a block from the file
                buffer = f.read(read_size)
                # Prepend the new block to existing data
                data = buffer + data
                # Update the remaining size
                remaining_size -= read_size
                # Split the data into lines
                lines = data.split(b'\n')

            # Decode lines and filter
            lines = [line.decode('utf-8', errors='ignore') for line in lines if line.strip()]
            target_lines = [line for line in reversed(lines) if 'python-requests' not in line]

            if not target_lines:
                logging.warning("No valid lines found in the log.")
                return None

            # Extract latencies from the last n valid lines
            for line in target_lines[:n]:
                try:
                    # Parse latency based on your log format
                    # Assuming the latency is the last field and in milliseconds
                    latency_str = line.split()[-1]
                    latency = float(latency_str)
                    latencies.append(latency)
                except (IndexError, ValueError) as parse_error:
                    logging.error(f"Error parsing latency from line: {line.strip()} - {parse_error}")
                    continue

            if not latencies:
                logging.warning("No valid latency values found.")
                return None

            # Calculate average latency
            average_latency = sum(latencies) / len(latencies)
            
            return average_latency / 1000

    except Exception as e:
        logging.error(f"Error reading latency from access log: {e}")
        return None

def adjust_thresholds(anomaly_label):
    """
    Adjust CPU and Memory thresholds based on anomaly detection.
    """
    global CPU_THRESHOLD_UPPER, MEMORY_THRESHOLD_UPPER, CPU_THRESHOLD_LOWER, MEMORY_THRESHOLD_LOWER

    if anomaly_label == -1:
        # Anomaly detected: decrease thresholds with a safety buffer
        safety_buffer_cpu = 5  # Percentage points
        safety_buffer_memory = 5  # Percentage points

        new_cpu_threshold_upper = max(CPU_THRESHOLD_UPPER - safety_buffer_cpu, 50)  # MIN_CPU_THRESHOLD = 50
        new_memory_threshold_upper = max(MEMORY_THRESHOLD_UPPER - safety_buffer_memory, 50)  # MIN_MEMORY_THRESHOLD = 50

        logging.info(f"Anomaly detected. Adjusting CPU Threshold Upper to {new_cpu_threshold_upper}%, Memory Threshold Upper to {new_memory_threshold_upper}%")
        print(f"[INFO] Anomaly detected. Adjusting CPU Threshold Upper to {new_cpu_threshold_upper}%, Memory Threshold Upper to {new_memory_threshold_upper}%")

        # Update global thresholds
        CPU_THRESHOLD_UPPER = new_cpu_threshold_upper
        MEMORY_THRESHOLD_UPPER = new_memory_threshold_upper
    else:
        # Normal operation: gradually increase thresholds if below maximum
        increment_cpu = 1  # Percentage points
        increment_memory = 1  # Percentage points

        new_cpu_threshold_upper = min(CPU_THRESHOLD_UPPER + increment_cpu, 90)  # MAX_CPU_THRESHOLD = 90
        new_memory_threshold_upper = min(MEMORY_THRESHOLD_UPPER + increment_memory, 90)  # MAX_MEMORY_THRESHOLD = 90

        logging.info(f"Normal operation. Adjusting CPU Threshold Upper to {new_cpu_threshold_upper}%, Memory Threshold Upper to {new_memory_threshold_upper}%")
        print(f"[INFO] Normal operation. Adjusting CPU Threshold Upper to {new_cpu_threshold_upper}%, Memory Threshold Upper to {new_memory_threshold_upper}%")

        # Update global thresholds
        CPU_THRESHOLD_UPPER = new_cpu_threshold_upper
        MEMORY_THRESHOLD_UPPER = new_memory_threshold_upper

    return CPU_THRESHOLD_UPPER, MEMORY_THRESHOLD_UPPER

# Function to create feature vector using OneHotEncoder
def create_feature_vector(avg_cpu, avg_memory, temp, weather_temp, humidity, req_per_sec, latency, weather_desc):
    try:
        # Prepare the categorical feature as a DataFrame with the correct column name
        weather_desc_df = pd.DataFrame({'Weather Description': [weather_desc]})
        weather_encoded = encoder.transform(weather_desc_df)
        weather_encoded_df = pd.DataFrame(
            weather_encoded, 
            columns=encoder.get_feature_names_out(['Weather Description'])
        )
        
        # Create the feature dictionary
        feature_vector = {
            'CPU Usage (%)': avg_cpu,
            'Memory Usage (%)': avg_memory,
            'CPU Temp (°C)': temp if temp != 'N/A' else 0,
            'Weather Temp (°C)': weather_temp if weather_temp else 0,
            'Humidity (%)': humidity if humidity else 0,
            'ReqPerSec': float(req_per_sec) if req_per_sec not in [None, 'N/A'] else 0,
            'Average Latency (ms)': float(latency) if latency else 0
        }
        
        # Combine with one-hot encoded weather descriptions
        feature_df = pd.concat([pd.DataFrame([feature_vector]), weather_encoded_df], axis=1)
        
        # Ensure all features are present
        for feature in FEATURES:
            if feature not in feature_df.columns:
                feature_df[feature] = 0  # Add missing features as 0
        
        # Reorder columns to match training
        feature_df = feature_df[FEATURES]
        
        return feature_df
    except Exception as e:
        logging.error(f"Error creating feature vector: {e}")
        return None
    
adaptation_history = deque(maxlen=10)  # Stores the last 10 adaptation states
state_durations = {'normal': 0, 'degraded': 0}
total_adaptations = 0

# Function to monitor system metrics
def monitor_metrics():
    previous_state = 'normal'
    current_state = 'normal'
    last_check_time = time.time()
    global adaptation_history, state_durations, total_adaptations 
    last_adaptation_time = 0

    # Initialize moving average deques
    CPU_HISTORY = deque(maxlen=6)  # e.g., last 1 minute if interval is 10s
    MEMORY_HISTORY = deque(maxlen=6)

    while True:
        try:
            current_time = time.time()
            time_diff = current_time - last_check_time
            last_check_time = current_time

            # Collect system metrics
            cpu_usage = psutil.cpu_percent(interval=0)
            memory_usage = calculate_memory_usage()
            temp = psutil.sensors_temperatures().get('cpu-thermal', [{}])[0].get('current', 'N/A')

            # Append to moving averages
            CPU_HISTORY.append(cpu_usage)
            MEMORY_HISTORY.append(memory_usage)

            # Compute moving averages
            avg_cpu = sum(CPU_HISTORY) / len(CPU_HISTORY)
            avg_memory = sum(MEMORY_HISTORY) / len(MEMORY_HISTORY)

            # Fetch weather data
            weather_temp, humidity, weather_desc = fetch_weather()

            # Fetch Apache metrics
            apache_metrics = fetch_apache_metrics()
            cache_hits = apache_metrics.get("CacheHits", "N/A") if apache_metrics else "N/A"
            cache_misses = apache_metrics.get("CacheMisses", "N/A") if apache_metrics else "N/A"
            req_per_sec = apache_metrics.get("ReqPerSec", "N/A") if apache_metrics else "N/A"
            busy_workers = apache_metrics.get("BusyWorkers", "N/A") if apache_metrics else "N/A"
            idle_workers = apache_metrics.get("IdleWorkers", "N/A") if apache_metrics else "N/A"

            # Fetch the latest latency from logs
            latency = get_average_latency(n=1000)
            latency_display = f"{latency:.2f} ms" if latency else "N/A"

            # Log the data
            logging.info(f"Avg CPU: {avg_cpu:.2f}%, Avg Memory: {avg_memory:.2f}%, Temp: {temp}°C, Latency: {latency_display}")
            logging.info(f"Weather: Temp: {weather_temp}°C, Humidity: {humidity}%, Desc: {weather_desc}")
            logging.info(f"Apache Metrics - ReqPerSec: {req_per_sec}, BusyWorkers: {busy_workers}, IdleWorkers: {idle_workers}, Cache Hits: {cache_hits}, Cache Misses: {cache_misses}")

            # Create feature vector for the model
            feature_df = create_feature_vector(avg_cpu, avg_memory, temp, weather_temp, humidity, req_per_sec, latency, weather_desc)

            if feature_df is None:
                logging.error("Feature vector creation failed. Skipping this iteration.")
                time.sleep(10)
                continue

            # Scale features
            try:
                scaled_features = scaler.transform(feature_df)
            except Exception as e:
                logging.error(f"Error scaling features: {e}")
                scaled_features = None

            if scaled_features is not None:
                # Log feature values
                logging.info(f"Feature Values: {feature_df.to_dict(orient='records')[0]}")

                # Predict anomaly
                try:
                    anomaly_label = model.predict(scaled_features)[0]  # -1 for anomaly, 1 for normal
                    logging.info(f"Anomaly Detection: {'Anomaly' if anomaly_label == -1 else 'Normal'}")
                except Exception as e:
                    logging.error(f"Error during anomaly prediction: {e}")
                    anomaly_label = 1  # Assume normal if prediction fails
            else:
                anomaly_label = 1  # Assume normal if scaling fails

            # Determine if adaptation is needed based on anomaly
            adaptation_needed = False
            switch_back = False

            if current_state == 'normal':
                if anomaly_label == -1:
                    adaptation_needed = True
            elif current_state == 'degraded':
                if anomaly_label == 1:
                    switch_back = True
            
            # Check cooldown
            time_since_last_adaptation = current_time - last_adaptation_time
            if (adaptation_needed or switch_back) and (time_since_last_adaptation >= COOLDOWN_PERIOD):
                # Adjust thresholds only if not in cooldown
                new_cpu_threshold, new_memory_threshold = adjust_thresholds(anomaly_label)
                # Update last adaptation time
                last_adaptation_time = current_time
            else:
                if (adaptation_needed or switch_back):
                    logging.info("Cooldown period active. Skipping adaptation.")
                    adaptation_needed = False
                    switch_back = False

            # Accumulate duration in current state
            state_durations[current_state] += time_diff

            previous_state = current_state
            # Proceed with updating adaptation state based on adaptation_needed and switch_back
            if adaptation_needed:
                current_state = 'degraded'
            elif switch_back:
                current_state = 'normal'

            # Check if the state has changed (adaptation occurred)
            adaptation_occurred = int(previous_state != current_state)
            
            if adaptation_occurred:
                # Update total adaptations count
                total_adaptations += 1
                # Update adaptation history
                adaptation_history.append((current_time, current_state))

            # Calculate adaptation frequency (number of adaptations in the last N entries)
            adaptation_frequency = sum(1 for _, state in adaptation_history if state == 'degraded')

            # Log the adaptation details
            logging.info(f"Adaptation Occurred: {adaptation_occurred}, Total Adaptations: {total_adaptations}, Adaptation Frequency: {adaptation_frequency}")
            logging.info(f"State Durations - Normal: {state_durations['normal']:.2f}s, Degraded: {state_durations['degraded']:.2f}s")

            # Save data to CSV with anomaly label and current thresholds
            # Save data to CSV with anomaly label and current thresholds
            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now(),
                    avg_cpu,
                    avg_memory,
                    temp,
                    weather_temp,
                    humidity,
                    weather_desc,
                    req_per_sec,
                    latency,
                    anomaly_label,
                    CPU_THRESHOLD_UPPER,
                    MEMORY_THRESHOLD_UPPER
                ])

            # Switch content based on anomaly
            switch_content(degrade=(current_state == 'degraded'))

            # Pause for 10 seconds before next reading
            time.sleep(10)

        except Exception as e:
            logging.error(f"Monitoring error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # Initialize CSV file with headers if it doesn't exist
    if not os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Timestamp",
                    "CPU Usage (%)",
                    "Memory Usage (%)",
                    "CPU Temp (°C)",
                    "Weather Temp (°C)",
                    "Humidity (%)",
                    "Weather Description",
                    "ReqPerSec",
                    # "BusyWorkers",
                    # "IdleWorkers",
                    # "Cache Hits",
                    # "Cache Misses",
                    "Average Latency (ms)",
                    # "Adaptation Occurred",
                    # "Total Adaptations",
                    # "Normal State Duration",
                    # "Degraded State Duration",
                    # "Adaptation Frequency",
                    # "Adaptation State",
                    #"CPU Threshold",
                    #"Memory Threshold",
                    "Anomaly Label",
                    "CPU Threshold Upper",
                    "Memory Threshold Upper"
                ])
        except Exception as e:
            logging.error(f"Error initializing CSV file: {e}")
            #print(f"[ERROR] Error initializing CSV file: {e}")

    # Start monitoring
    monitor_metrics()
