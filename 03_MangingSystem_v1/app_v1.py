from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime
import os, time, threading, sys
import json
from datetime import datetime
## Import external functions
utils_path = os.path.join(os.path.dirname(__file__), '.', 'components')
sys.path.append(utils_path)
from module1_get_weather import extern_get_weather
from module2_get_cpu_memory import extern_get_cpu_memory_usage
from module3_get_random_color import extern_get_random_color
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

def extern_foo1_dummy_task():
    print(f'## this is {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

# Periodic task for foo1
def run_foo1_periodically():
    while True:
        extern_foo1_dummy_task()  # Call foo1
        time.sleep(10)  # Wait 10 seconds


if __name__ == "__main__":
    threading.Thread(target=run_foo1_periodically, daemon=True).start() #daemon=True ensures that the threads terminate automatically when the main program exits
    app.run(host="0.0.0.0", port=5000)