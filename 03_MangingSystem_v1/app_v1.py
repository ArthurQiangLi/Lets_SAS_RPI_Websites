from flask import Flask, render_template, jsonify, request
import psutil
import random
import requests
from datetime import datetime
import os, time, threading
import json
from datetime import datetime
## Import external functions
#from foo1 import foo1  # Import foo1 from foo1.py
#from foo2 import foo2  # Import foo2 from foo2.py

## Reads config.json during startup 
with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/background_color", methods=["GET"])
def background_color():
    return jsonify({"color": extern_get_random_color()})

@app.route("/weather", methods=["GET"])
def weather():
    return jsonify({"weather": extern_get_weather(config["city"])})

@app.route("/cpu_stats", methods=["GET"])
def cpu_stats():
    return jsonify(extern_get_cpu_memory_usage())


@app.route("/reboot", methods=["POST"])
def reboot():
    os.system("sudo reboot")
    return "Rebooting the Raspberry Pi...", 200

### Extern functions 
def extern_get_weather(city):
    return "22°C, Clear Skies"

def extern_get_cpu_memory_usage():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent
    }

def extern_get_random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

def extern_foo1_dummy_task():
    print(f'## this is {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

# Periodic task for foo1
def run_foo1_periodically():
    while True:
        extern_foo1_dummy_task()  # Call foo1
        time.sleep(10)  # Wait 10 seconds


if __name__ == "__main__":
    # threading.Thread(target=run_foo1_periodically, daemon=True).start() #daemon=True ensures that the threads terminate automatically when the main program exits
    app.run(host="0.0.00.", port=5000)