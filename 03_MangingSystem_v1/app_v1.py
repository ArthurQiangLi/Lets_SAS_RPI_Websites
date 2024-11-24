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

@app.route("/")
def dashboard():
    age = "18.888"
    return render_template("dashboard.html", age=age)

@app.route("/background_color", methods=["GET"])
def background_color():
    return jsonify({"color": get_random_color()})

@app.route("/weather", methods=["GET"])
def weather():
    return jsonify({"weather": get_weather(config["city"])})

@app.route("/cpu_stats", methods=["GET"])
def cpu_stats():
    return jsonify(get_cpu_memory_usage())

def get_random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

def get_weather(city):
    # Replace with a valid weather API implementation
    return "22°C, Clear Skies"

def get_cpu_memory_usage():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)