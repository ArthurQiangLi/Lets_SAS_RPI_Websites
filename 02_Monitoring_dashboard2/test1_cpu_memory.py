import psutil
import time
import logging
import csv
import os
from datetime import datetime

# Configure logging
logging.basicConfig(filename="cpu_memory_monitor.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Constants
CSV_FILE = "cpu_memory_metrics.csv"

# Degradation Thresholds (if needed for alerts)
CPU_THRESHOLD = 80  # in percentage
MEMORY_THRESHOLD = 90  # in percentage

# Flag to determine memory mode (True = total memory usage, False = actual memory usage)
USE_TOTAL_MEMORY = False

# Function to calculate memory usage
def calculate_memory_usage():
    memory = psutil.virtual_memory()
    if USE_TOTAL_MEMORY:
        return memory.percent
    else:
        # Calculate actual memory usage excluding buffers and cache
        actual_memory_percent = 100 * (memory.used - memory.buffers - memory.cached) / memory.total
        return actual_memory_percent

# Function to monitor CPU and memory usage
def monitor_cpu_memory():
    while True:
        try:
            # Collect system metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = calculate_memory_usage()

            # Log the data
            logging.info(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage:.2f}%")

            # Save data to CSV
            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now(),
                    cpu_usage,
                    memory_usage
                ])

            # You can add alerting logic here if thresholds are exceeded
            # For example:
            if cpu_usage > CPU_THRESHOLD:
                logging.warning(f"High CPU usage detected: {cpu_usage}%")
            if memory_usage > MEMORY_THRESHOLD:
                logging.warning(f"High Memory usage detected: {memory_usage:.2f}%")

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
                    "CPU Usage (%)",
                    "Memory Usage (%)"
                ])
        except Exception as e:
            logging.error(f"Error initializing CSV file: {e}")
            print(f"[ERROR] Error initializing CSV file: {e}")

    # Start monitoring
    monitor_cpu_memory()
