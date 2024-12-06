import os
import csv
from datetime import datetime

# Global variables to track current log files
current_a10_file = None
current_a30_file = None

def pick_wanted(input_dict):
    # Define the items you want to pick
    wanted_keys = ["cpu", "cpu_temperature", "memory", "apache2metrics_BusyWorkers","apache2metrics_Load1","apache2metrics_DurationPerReq",  "health", "performance", "no", "clock"]
    
    # Initialize the output dictionary
    picked = {}
    
    for key in wanted_keys:
        # Check if the key exists in the input_dict; if not, add it with an empty value
        picked[key] = input_dict.get(key, "")
    
    return picked


# Function to check file size and create a new file if needed
def check_or_create_file(prefix):
    global current_a10_file, current_a30_file
    
    # Determine the file to check
    if prefix == "a10":
        current_file = current_a10_file
    elif prefix == "a30":
        current_file = current_a30_file
    else:
        raise ValueError("Invalid prefix. Use 'a10' or 'a30'.")

    # Create a new file if no file exists or file exceeds 2 MB
    if current_file is None or not os.path.exists(current_file) or os.path.getsize(current_file) > 2 * 1024 * 1024:
        filename = f"logged_data/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{prefix}.csv"
        os.makedirs("logged_data", exist_ok=True)  # Ensure directory exists
        if prefix == "a10":
            current_a10_file = filename
        elif prefix == "a30":
            current_a30_file = filename
        return filename

    return current_file


# Function to log a10 data every 10 seconds
def extern_log_a10_data(a10):
    global current_a10_file
    current_a10_file = check_or_create_file("a10")  # Get or create a valid file

    # Write data to the CSV file
    with open(current_a10_file, mode="a", newline="") as file:  # Append mode
        writer = csv.writer(file)
        if file.tell() == 0:  # If the file is empty, write the header
            writer.writerow(["Timestamp"] + list(a10.keys()))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp] + list(a10.values()))
    print(f"a10 data logged to {current_a10_file}")


# Function to log a30 data every 30 seconds
def extern_log_a30_data(a30):
    global current_a30_file
    current_a30_file = check_or_create_file("a30")  # Get or create a valid file

    # Write data to the CSV file
    with open(current_a30_file, mode="a", newline="") as file:  # Append mode
        writer = csv.writer(file)
        if file.tell() == 0:  # If the file is empty, write the header
            writer.writerow(["Timestamp"] + list(a30.keys()))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp] + list(a30.values()))
    print(f"a30 data logged to {current_a30_file}")


def extern_flatten_dict(d, parent_key='', sep='_'):
    """
    Flattens a multi-level dictionary into a single-layer dictionary.
    
    :param d: Dictionary to flatten
    :param parent_key: String to use as prefix for keys (used for recursion)
    :param sep: Separator to use for nested keys
    :return: Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k  # Create new key
        if isinstance(v, dict):  # If value is a dictionary, recurse
            items.extend(extern_flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Example usage
# a = {"a": 1, "b": 2, "c": {"d": True, "e": False}}
# flattened_a = flatten_dict(a)
# print(flattened_a)



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