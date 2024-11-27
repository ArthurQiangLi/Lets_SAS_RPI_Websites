import requests
import logging

APACHE_STATUS_URL = "http://localhost/server-status?auto"
NETWORK_TIMEOUT = 5  # seconds

def extern_fetch_apache_metrics():
    try:
        response = requests.get(APACHE_STATUS_URL, timeout=NETWORK_TIMEOUT)
        if response.status_code == 200:
            return parse_apache_status(response.text)
        else:
            logging.error(f"Failed to fetch Apache metrics: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error fetching Apache metrics: {e}")
        return None

#Parses Apache server status text into a dictionary.
def parse_apache_status(status_text):
    status_dict = {}
    for line in status_text.splitlines():
        if ": " in line:  # Only process lines with key-value pairs
            key, value = line.split(": ", 1)
            key = key.replace(" ", "")  # Remove spaces in keys
            try:
                # Convert numeric values to appropriate types
                if "." in value:
                    status_dict[key] = float(value)
                else:
                    status_dict[key] = int(value)
            except ValueError:
                status_dict[key] = value  # Keep as string if conversion fails
    return status_dict

# Extracts specific metrics into a sub-dictionary.
def extract_specific_metrics(status_dict):
    keys_to_extract = [
        "ServerUptimeSeconds",
        "TotalAccesses",
        "TotalkBytes",
        "BusyWorkers",
        "IdleWorkers",
        "Processes",
        "ConnsTotal",
    ]
    m = {key: status_dict[key] for key in keys_to_extract if key in status_dict}
    return m


def format_seconds_to_readable(seconds):
    """
    Convert seconds into a human-readable format of 'Xd Xh Xm Xs'.
    """
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

def extern_get_apache2metrics():
    m = extern_fetch_apache_metrics()
    a = extract_specific_metrics(m)
    server_uptime_seconds = a.pop("ServerUptimeSeconds")  # Remove the old key
    a["ServerUptime"] = format_seconds_to_readable(server_uptime_seconds)  # Add the new key    
    return a
    # return {'ServerUptime': '2 days 23 hours 7 minutes 8 seconds', 'TotalAccesses': 664, 'TotalkBytes': 3973, 'BusyWorkers': 1, 'IdleWorkers': 49, 'Processes': 2, 'ConnsTotal': 1}
# Apache status text
# apache_status_text = """
# localhost
# ServerVersion: Apache/2.4.62 (Raspbian)
# ServerMPM: event
# Server Built: 2024-10-04T15:21:08
# CurrentTime: Tuesday, 26-Nov-2024 18:29:51 CST
# RestartTime: Saturday, 23-Nov-2024 19:22:42 CST
# ParentServerConfigGeneration: 4
# ParentServerMPMGeneration: 3
# ServerUptimeSeconds: 256028
# ServerUptime: 2 days 23 hours 7 minutes 8 seconds
# Load1: 0.39
# Load5: 0.48
# Load15: 0.50
# Total Accesses: 664
# Total kBytes: 3973
# Total Duration: 1372
# CPUUser: 10.35
# CPUSystem: 16.46
# CPUChildrenUser: .82
# CPUChildrenSystem: .67
# CPULoad: .0110535
# Uptime: 256028
# ReqPerSec: .00259347
# BytesPerSec: 15.8903
# BytesPerReq: 6127.04
# DurationPerReq: 2.06627
# BusyWorkers: 1
# GracefulWorkers: 0
# IdleWorkers: 49
# Processes: 2
# Stopping: 0
# ConnsTotal: 1
# ConnsAsyncWriting: 0
# ConnsAsyncKeepAlive: 1
# ConnsAsyncClosing: 0
# Scoreboard: _W________________________________________________....................................................................................................
# """

# # Step 1: Parse the text into a dictionary
# status_dict = parse_apache_status(apache_status_text)
# print("Parsed Dictionary:")
# print(status_dict)

# # Step 2: Extract specific metrics
# metrics = extract_specific_metrics(status_dict)
# print("\nExtracted Metrics:")
# print(metrics)
