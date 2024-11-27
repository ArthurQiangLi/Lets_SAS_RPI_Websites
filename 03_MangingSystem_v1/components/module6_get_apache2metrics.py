import requests
import logging

APACHE_STATUS_URL = "http://localhost/server-status?auto"
NETWORK_TIMEOUT = 5  # seconds

def extern_fetch_apache_metrics():
    try:
        response = requests.get(APACHE_STATUS_URL, timeout=NETWORK_TIMEOUT)
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


def get_wanted_metrics(metrics):
    if(metrics):
        m = {} #make a new empty dictionary
        m["ServerUptime"] = metrics["ServerUptime"]