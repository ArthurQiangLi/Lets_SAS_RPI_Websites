import os
import csv
from datetime import datetime

# Function to log a10 data every 10 seconds
def extern_log_a10_data(a10):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"logged_data/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_a10.csv"
    os.makedirs("logged_data", exist_ok=True)  # Ensure directory exists

    # Write data to the CSV file
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp"] + list(a10.keys()))  # Header row
        writer.writerow([timestamp] + list(a10.values()))  # Data row
    print(f"a10 data logged to {filename}")

# Function to log a30 data every 30 seconds
def extern_log_a30_data(a30):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"logged_data/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_a30.csv"
    os.makedirs("logged_data", exist_ok=True)  # Ensure directory exists

    # Write data to the CSV file
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp"] + list(a30.keys()))  # Header row
        writer.writerow([timestamp] + list(a30.values()))  # Data row
    print(f"a30 data logged to {filename}")


# 📦03_MangingSystem_v1
#  ┣ 📂components
#  ┃ ┗ 📜module80_logging.py 
#  ┣ 📂components
#  ┃ ┗ 📜logging files
#  ┣ 📂static
#  ┃ ┣ 📜script.js
#  ┃ ┗ 📜style.css
#  ┣ 📂templates
#  ┃ ┗ 📜dashboard.html
#  ┣ 📜app_v1.md
#  ┣ 📜app_v1.py
#  ┗ 📜config.json