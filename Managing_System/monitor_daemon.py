import psutil
import requests
import time
import logging
import csv
import os
import shutil
import subprocess

from datetime import datetime

APACHE_STATUS_URL = "http://localhost/server-status?auto"
ACCESS_LOG_FILE = "/var/log/apache2/access.log"

# Configure logging
logging.basicConfig(filename="monitoring.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Constants
WEATHER_API_KEY = "7a8fdd951ab780e11ad83ac773f07e7f"  # Replace with your actual API key
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
LOCATION = "Kitchener,CA"  # Replace with your city and country code
CSV_FILE = "system_metrics.csv"

# Degradation Thresholds
CPU_THRESHOLD = 15  # in percentage
MEMORY_THRESHOLD = 90  # in percentage

# Paths to HTML files
CURRENT_HTML = "/var/www/html/index.html"
HIGH_LOAD_HTML = "/var/www/html/high_load.html"
NORMAL_CONTENT_HTML = "/var/www/html/normal_content.html"

# Flag to determine memory mode (True = total memory usage, False = actual memory usage)
USE_TOTAL_MEMORY = False

# Set timeouts for network requests
NETWORK_TIMEOUT = 5  # seconds

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
        print(degrade)
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
        os.utime(CURRENT_HTML, None)
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
def get_latest_latency():
    try:
        with open(ACCESS_LOG_FILE, 'rb') as file:
            lines_to_read = 100
            buffer = bytearray()
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            block_size = 1024
            lines_found = 0
            while file_size > 0 and lines_found < lines_to_read:
                if file_size - block_size > 0:
                    file.seek(file_size - block_size)
                    block = file.read(block_size)
                else:
                    file.seek(0)
                    block = file.read(file_size)
                buffer.extend(block)
                lines_found = buffer.count(b'\n')
                file_size -= block_size
            all_read_text = buffer.decode('utf-8', errors='ignore')
            lines = all_read_text.splitlines()
            # Filter out monitoring daemon requests
            target_lines = [line for line in lines if 'python-requests' not in line]
            if not target_lines:
                return None
            last_line = target_lines[-1]
            latency = int(last_line.split()[-1])  # Adjust based on your log format
            return latency / 1000
    except Exception as e:
        logging.error(f"Error reading latency from access log: {e}")
        return None

# Function to monitor system metrics
def monitor_metrics():
    while True:
        try:
            # Collect system metrics
            cpu_usage = psutil.cpu_percent(interval=0)
            memory_usage = calculate_memory_usage()
            temp = psutil.sensors_temperatures().get('cpu-thermal', [{}])[0].get('current', 'N/A')

            print(cpu_usage)
            print(memory_usage)

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
            latency = get_latest_latency()
            latency_display = f"{latency:.2f} ms" if latency else "N/A"

            # Log the data
            logging.info(f"CPU: {cpu_usage}%, Memory: {memory_usage:.2f}%, Temp: {temp}°C, Latency: {latency_display}")
            logging.info(f"Weather: Temp: {weather_temp}°C, Humidity: {humidity}%, Desc: {weather_desc}")
            logging.info(f"Apache Metrics - ReqPerSec: {req_per_sec}, BusyWorkers: {busy_workers}, IdleWorkers: {idle_workers}, Cache Hits: {cache_hits}, Cache Misses: {cache_misses}")

            # Save data to CSV
            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now(),
                    cpu_usage,
                    memory_usage,
                    temp,
                    weather_temp,
                    humidity,
                    weather_desc,
                    req_per_sec,
                    busy_workers,
                    idle_workers,
                    cache_hits,
                    cache_misses,
                    latency
                ])

            # Degrade content based on thresholds
            if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD:
                switch_content(degrade=True)
            else:
                switch_content(degrade=False)

            # Pause for 15 seconds before next reading
            time.sleep(15)

        except Exception as e:
            logging.error(f"Monitoring error: {e}")
            #print(f"[ERROR] Monitoring error: {e}")
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
                    "BusyWorkers",
                    "IdleWorkers",
                    "Cache Hits",
                    "Cache Misses",
                    "Latency (ms)"
                ])
        except Exception as e:
            logging.error(f"Error initializing CSV file: {e}")
            #print(f"[ERROR] Error initializing CSV file: {e}")

    # Start monitoring
    monitor_metrics()
