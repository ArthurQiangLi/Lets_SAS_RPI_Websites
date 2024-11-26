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
from module2_get_cpu_memory import extern_get_arm_clock
from module2_get_cpu_memory import extern_get_pi_throttled_status
from module2_get_cpu_memory import extern_get_apache_active
from module3_get_random_color import extern_get_random_color
from module4_get_run_age import extern_get_age
from module5_get_cpu_temperature import extern_get_cpu_temperature1
from module51_set_reboot import extern_set_reboot
from module52_set_cpu_clock import extern_set_governor2
from module53_set_watchdog import extern_watchdog
## Reads config.json during startup 
with open("config.json", "r") as f:
    config = json.load(f)
### local global data.
contraol_data = {"is_watchdog": False}
app = Flask(__name__)
### get on starting
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

### get every 1s
@app.route("/update_1s", methods=["GET"]) 
def cpu_stats():
    status = extern_get_cpu_memory_usage() # returns {"cpu": 22, "memory": 60} dictionary
    status["cpu_temperature"] = extern_get_cpu_temperature1() #return int 60 in celcuis
    status["arm_clock"] = extern_get_arm_clock() #return int 600, means 600Mhz
    status["total_cpu"] = status["arm_clock"] * int(status["cpu"]) * 0.01 # because cpu is 0..100
    status["throttled_status"]= extern_get_pi_throttled_status() #return a boolean dictionary {"under_voltage": True, ...}
    status["color"] = extern_get_random_color() # return int 0xababab
    status["age"] = extern_get_age() #return string '5d, 0h, 52m, 53s'
    return jsonify(status)

### get every 10s
@app.route("/update_10s", methods=["GET"])
def background_color():
    status = {}
    status["apache_active"] = extern_get_apache_active() # bool, true=active, false=stopped
    status["watchdog"] = contraol_data["is_watchdog"]
    return jsonify(status)

### get every 30s
@app.route("/update_30s", methods=["GET"]) 
def weather():
    weather = extern_fetch_weather() #return {"temp":-3, "humidity": 98, "weather":mist}
    return jsonify(weather)

### On click
@app.route("/reboot", methods=["POST"])
def reboot():
    extern_set_reboot()
    return "Rebooting the Raspberry Pi...", 200

@app.route("/min_clock", methods=["POST"])
def min_clock():
    extern_set_governor2("powersave")
    return "Setting powersave (min clock)...", 200

@app.route("/max_clock", methods=["POST"])
def max_clock():
    extern_set_governor2("performance")
    return "Setting max clock...", 200

@app.route("/on_demand", methods=["POST"])
def auto_clock():
    extern_set_governor2("ondemand")
    return "Setting ondemand (default clock)...", 200

@app.route("/watchdog", methods=["POST"])
def switch_watchdog():
    en = not contraol_data["is_watchdog"]
    contraol_data["is_watchdog"] =  en
    return f"Now watched dog is {en} status.", 200

# Periodic task for foo1: watchdog thread
def foo1_thread():
    while True:
        check_interval_seconds = 10  # Check every 10 seconds
        downtime_threshold = 120  # Reboot if service is down for 120 seconds
        extern_watchdog("apache2", downtime_threshold, check_interval_seconds)  # Call foo1
        time.sleep(check_interval_seconds)  # Wait 10 seconds


if __name__ == "__main__":
    threading.Thread(target=foo1_thread, daemon=True).start() #daemon=True ensures that the threads terminate automatically when the main program exits
    app.run(host="0.0.0.0", port=5000)

