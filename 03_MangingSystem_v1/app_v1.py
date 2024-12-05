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
from module6_get_apache2metrics import extern_get_apache2metrics
from module51_set_reboot import extern_set_reboot
from module52_set_cpu_clock import extern_set_governor2
from module53_set_watchdog import extern_watchdog
from module70_mapek import mape_monitoring, mape_analyzing, mape_planning
from module80_logging import extern_log_a10_data, extern_log_a30_data, extern_flatten_dict
## Reads config.json during startup 
with open("config.json", "r") as f:
    config = json.load(f)
### local global data.
control_data = {"is_watchdog": True}
status1s = {}
mapek = {}
flat_d30s = {}
flat_d1s = {}
dic_flat_allmatrics = {}
plan = {"no": 1,  # = 1/2/3/4
        "clock": 'min'} # = min/max
app = Flask(__name__)
### get on starting
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

### get every 1s
@app.route("/update_1s", methods=["GET"]) 
def cpu_stats():
    global status1s
    status1s = extern_get_cpu_memory_usage() # returns {"cpu": 22, "memory": 60} dictionary
    status1s["cpu_temperature"] = extern_get_cpu_temperature1() #return int 60 in celcuis
    status1s["arm_clock"] = extern_get_arm_clock() #return int 600, means 600Mhz
    status1s["total_cpu"] = status1s["arm_clock"] * int(status1s["cpu"]) * 0.01 # because cpu is 0..100
    status1s["throttled_status"]= extern_get_pi_throttled_status() #return a boolean dictionary {"under_voltage": True, ...}
    status1s["color"] = extern_get_random_color() # return int 0xababab
    status1s["age"] = extern_get_age() #return string '5d, 0h, 52m, 53s'
    status1s["watchdog"] = control_data["is_watchdog"]
    status1s["apache_active"] = extern_get_apache_active()
    return jsonify(status1s)

### get every 10s
@app.route("/update_10s", methods=["GET"])
def background_color():
    global flat_d1s
    global flat_d30s # set global to let mape() uses it.
    global dic_flat_allmatrics
    status10s = extern_fetch_weather() #return {"temp":-3, "humidity": 98, "weather":mist}
    status10s["apache2metrics"] = extern_get_apache2metrics()
    flat_d30s = extern_flatten_dict(status10s)
    flat_d1s = extern_flatten_dict(status1s)
    dic_flat_allmatrics = flat_d1s|flat_d30s
    extern_log_a10_data(flat_d1s|flat_d30s|mapek) ## log data
    return jsonify(status10s)

### get every 30s
@app.route("/update_30s", methods=["GET"]) 
def weather():
    status30s = extern_fetch_weather() #return {"temp":-3, "humidity": 98, "weather":mist}
    flat_d30s = extern_flatten_dict(status30s)
    flat_d1s = extern_flatten_dict(status1s)
    extern_log_a10_data(flat_d1s|flat_d30s)
    return jsonify(status30s)

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
    en = control_data["is_watchdog"]
    control_data["is_watchdog"] =  not en
    return f"Now switching watchdog.", 200

# Periodic task for foo1: watchdog thread, executed every 10 second.
def foo1_thread():
    global mapek  # use this global data here and log in '@30s'
    global plan
    while control_data["is_watchdog"]: # when the switch is on (by default)
        ##[1] watchdog
        check_interval_seconds = 10  # Check every 10 seconds
        downtime_threshold = 120  # Reboot if service is down for 120 seconds
        extern_watchdog("apache2", downtime_threshold, check_interval_seconds) 

        ##[2] Rule-based adaptation
        # collect metrics: cpu, memory, cpu-temperature/  apache-load1, busyworkers(1~50), durationPerReq(ms)
        metric = mape_monitoring(dic_flat_allmatrics)
        # calculate utilities
        state = mape_analyzing(metric)
        # planning
        plan = mape_planning(metric, state, plan)
        # executing
        mapek = state | plan  # log data to plot

        time.sleep(check_interval_seconds)  # Wait 10 seconds


if __name__ == "__main__":
    threading.Thread(target=foo1_thread, daemon=True).start() #daemon=True ensures that the threads terminate automatically when the main program exits
    app.run(host="0.0.0.0", port=5000)

