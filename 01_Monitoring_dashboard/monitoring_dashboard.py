from flask import Flask, render_template, jsonify, request
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
    if "weather" in data and "main" in data:
        return f"{data['weather'][0]['description'].capitalize()}, {data['main']['temp']}°C"
    return "Weather data unavailable"

def get_cpu_memory_usage():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    return {"cpu": cpu, "memory": memory.percent}

def calculate_age(birthday):
    birth_date = datetime.strptime(birthday, "%Y-%m-%d")
    age_days = (datetime.now() - birth_date).days
    age_years = age_days / 365.25
    return f"{age_years:.3f} yr"

@app.route("/")
def dashboard():
    weather = get_weather(config["city"])
    age = calculate_age(config["birthday"])
    stats = get_cpu_memory_usage()
    color = get_random_color()
    return render_template(
        "dashboard.html", 
        weather=weather, 
        age=age, 
        stats=stats, 
        color=color
    )

@app.route("/reboot", methods=["POST"])
def reboot():
    os.system("sudo reboot")
    return "Rebooting..."

@app.route("/background_color", methods=["GET"])
def background_color():
    return jsonify({"color": get_random_color()})

def get_random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
