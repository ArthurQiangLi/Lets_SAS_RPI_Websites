import requests
import time
import logging
import csv
import os
from datetime import datetime

APACHE_STATUS_URL = "http://localhost/server-status?auto"

# Configure logging
logging.basicConfig(filename="apache_metrics_monitor.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Constants
CSV_FILE = "apache_metrics.csv"

# Function to fetch Apache metrics
def fetch_apache_metrics():
    try:
        response = requests.get(APACHE_STATUS_URL)
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

# Function to monitor Apache metrics
def monitor_apache_metrics():
    while True:
        try:
            # Fetch Apache metrics
            apache_metrics = fetch_apache_metrics()
            if apache_metrics:
                req_per_sec = apache_metrics.get("ReqPerSec", "N/A")
                busy_workers = apache_metrics.get("BusyWorkers", "N/A")
                idle_workers = apache_metrics.get("IdleWorkers", "N/A")

                # Log the data
                logging.info(f"ReqPerSec: {req_per_sec}, BusyWorkers: {busy_workers}, IdleWorkers: {idle_workers}")

                # Save data to CSV
                with open(CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        datetime.now(),
                        req_per_sec,
                        busy_workers,
                        idle_workers
                    ])
            else:
                logging.error("No Apache metrics retrieved.")

            # Pause before next reading
            time.sleep(5)

        except Exception as e:
            logging.error(f"Monitoring error: {e}")
            print(f"[ERROR] Monitoring error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    # Initialize CSV file with headers if it doesn't exist
    if not os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Timestamp",
                    "ReqPerSec",
                    "BusyWorkers",
                    "IdleWorkers"
                ])
        except Exception as e:
            logging.error(f"Error initializing CSV file: {e}")
            print(f"[ERROR] Error initializing CSV file: {e}")

    # Start monitoring
    monitor_apache_metrics()
