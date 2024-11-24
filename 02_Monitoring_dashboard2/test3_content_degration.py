import psutil
import time
import logging
import os
import shutil

# Configure logging
logging.basicConfig(filename="content_degradation.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Degradation Thresholds
CPU_THRESHOLD = 80  # in percentage
MEMORY_THRESHOLD = 90  # in percentage

# Paths to HTML files
CURRENT_HTML = "/var/www/html/index.html"
HIGH_LOAD_HTML = "/var/www/html/high_load.html"
NORMAL_CONTENT_HTML = "/var/www/html/normal_content.html"

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

# Function to switch content based on system load
def switch_content(degrade=False):
    try:
        # Determine the target content
        target_content_path = HIGH_LOAD_HTML if degrade else NORMAL_CONTENT_HTML

        # Read the contents of CURRENT_HTML
        with open(CURRENT_HTML, 'r') as current_file:
            current_content = current_file.read()

        # Read the contents of the target content
        with open(target_content_path, 'r') as target_file:
            target_content = target_file.read()

        # Check if the contents are the same
        if current_content == target_content:
            logging.info("Content already matches the target. No changes made.")
            print("[INFO] Content already matches the target. No changes made.")
            return

        # Switch the content by copying the target file to CURRENT_HTML
        shutil.copyfile(target_content_path, CURRENT_HTML)
        logging.info(f"Content switched to {'high_load.html' if degrade else 'normal_content.html'}")
        print(f"[INFO] Content switched to {'high_load.html' if degrade else 'normal_content.html'}")
    except Exception as e:
        logging.error(f"Error switching content: {e}")
        print(f"[ERROR] Error switching content: {e}")

# Function to monitor system metrics and switch content
def monitor_and_switch_content():
    while True:
        try:
            # Collect system metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = calculate_memory_usage()

            # Log the data
            logging.info(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage:.2f}%")

            # Degrade content based on thresholds
            if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD:
                switch_content(degrade=True)
            else:
                switch_content(degrade=False)

            # Pause before next reading
            time.sleep(5)

        except Exception as e:
            logging.error(f"Monitoring error: {e}")
            print(f"[ERROR] Monitoring error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    # Ensure that the script has permissions to modify the web content
    if not os.access(CURRENT_HTML, os.W_OK):
        logging.error(f"Permission denied: Cannot write to {CURRENT_HTML}")
        print(f"[ERROR] Permission denied: Cannot write to {CURRENT_HTML}")
    else:
        # Start monitoring and switching content
        monitor_and_switch_content()
