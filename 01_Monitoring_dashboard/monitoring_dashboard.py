from flask import Flask, render_template, request
import psutil
import random
import requests
from datetime import datetime
import os
import json

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)

def get_weather(city):
    API_KEY = config["openweather_api_key"]
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    weather = f"{data['weather'][0]['description'].capitalize()}, {data['main']['temp']}°C"
    return weather

def get_cpu_memory_usage():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    return f"CPU: {cpu}%, Memory: {memory.percent}%"

def get_bus_info():
    # Replace with actual API calls for your local transit information
    station_1 = "Station A: Bus 101 in 5 mins, Bus 202 in 10 mins"
    station_2 = "Station B: Bus 303 in 3 mins, Bus 404 in 12 mins"
    return station_1, station_2

def calculate_age(birthday):
    birth_date = datetime.strptime(birthday, "%Y-%m-%d")
    age_days = (datetime.now() - birth_date).days
    age_years = age_days / 365.25
    return f"{age_years:.3f} yr"

def get_random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

@app.route("/")
def dashboard():
    weather = get_weather(config["city"])
    cpu_memory = get_cpu_memory_usage()
    station_1, station_2 = get_bus_info()
    age = calculate_age(config["birthday"])
    color = get_random_color()
    return render_template(
        "dashboard.html",
        weather=weather,
        cpu_memory=cpu_memory,
        station_1=station_1,
        station_2=station_2,
        age=age,
        color=color,
    )

@app.route("/reboot", methods=["POST"])
def reboot():
    os.system("sudo reboot")
    return "Rebooting..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
