from flask import Flask, render_template, jsonify, request
import requests
import os, time, threading, sys
import json
from datetime import datetime
## Import external functions
utils_path = os.path.join(os.path.dirname(__file__), '.', 'components')
sys.path.append(utils_path)
from module1_get_weather import extern_fetch_weather
from module2_get_cpu_memory import extern_get_cpu_memory_usage
from module3_get_random_color import extern_get_random_color
from module5_get_cpu_temperature import extern_get_cpu_temperature1
from module51_set_reboot import extern_set_reboot
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
    temp, humidity, weather = extern_fetch_weather()
    return jsonify({"temp":temp, "humidity": humidity, "weather":weather})

@app.route("/cpu_stats", methods=["GET"])
def cpu_stats():
    status = extern_get_cpu_memory_usage()
    temperature = extern_get_cpu_temperature1() # tempearture = '60' in celcuis
    status["cpu_temperature"] = temperature # add 'cpu-temperature' into status dictionary
    return jsonify(status)

@app.route("/reboot", methods=["POST"])
def reboot():
    extern_set_reboot()
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