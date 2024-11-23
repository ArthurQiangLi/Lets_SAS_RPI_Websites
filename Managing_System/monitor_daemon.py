import psutil
import requests
import time
import logging
import csv
from datetime import datetime

# Configure logging
logging.basicConfig(filename="monitoring.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Constants
WEATHER_API_KEY = "7a8fdd951ab780e11ad83ac773f07e7f"  # API key
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
LOCATION = "Kitchener,CA"  # Replace with your city and country code

# CSV file to store historical data
CSV_FILE = "system_metrics.csv"

# Function to fetch weather data
def fetch_weather():
    try:
        response = requests.get(WEATHER_API_URL, params={
            "q": LOCATION,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        })
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

# Function to monitor system metrics
def monitor_metrics():
    while True:
        try:
            # Collect system metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            temp = psutil.sensors_temperatures().get('cpu-thermal', [{}])[0].get('current', 'N/A')

            # Fetch weather data
            weather_temp, humidity, weather_desc = fetch_weather()

            # Log the data
            logging.info(f"CPU: {cpu_usage}%, Memory: {memory.percent}%, Temp: {temp}°C")
            logging.info(f"Weather: Temp: {weather_temp}°C, Humidity: {humidity}%, Desc: {weather_desc}")

            # Save data to CSV
            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.now(), cpu_usage, memory.percent, temp, weather_temp, humidity, weather_desc])

            # Pause for 10 seconds before next reading
            time.sleep(2)

        except Exception as e:
            logging.error(f"Monitoring error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    # Initialize CSV file with headers if it doesn't exist
    try:
        with open(CSV_FILE, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "CPU Usage (%)", "Memory Usage (%)", "CPU Temp (°C)", "Weather Temp (°C)", "Humidity (%)", "Weather Description"])
    except FileExistsError:
        pass

    # Start monitoring
    monitor_metrics()
