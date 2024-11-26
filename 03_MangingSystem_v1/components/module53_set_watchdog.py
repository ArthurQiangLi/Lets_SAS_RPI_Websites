import time
import subprocess

# Returns: bool: True if the service is active, False otherwise.
def check_service_status(service_name):
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip() == "active"
    except Exception as e:
        print(f"Error checking service status: {e}")
        return False

def reboot_system():
    print("Rebooting the system...")
    subprocess.run(["sudo", "reboot"])

"""
Monitor the given service and reboot the system if the service is down for a specified timeout.
Args:
    service_name (str): The name of the service to monitor.
    timeout (int): Time in seconds to allow the service to remain inactive before rebooting.
    check_interval (int): Time in seconds between checks.
"""
def extern_watchdog(service_name, timeout, check_interval):
    down_time = 0

    while True:
        if check_service_status(service_name):
            print(f"{service_name} is active.")
            down_time = 0  # Reset down time if the service is active
        else:
            down_time += check_interval
            print(f"{service_name} is inactive. Down time: {down_time}s")

            if down_time >= timeout:
                print(f"{service_name} has been down for {timeout}s. Triggering reboot.")
                reboot_system()
                break  # Exit loop after reboot command

        time.sleep(check_interval)

# if __name__ == "__main__":
#     # Configuration
#     service_to_monitor = "apache2"
#     downtime_threshold = 120  # Reboot if service is down for 120 seconds
#     check_interval_seconds = 10  # Check every 10 seconds

#     print(f"Starting watchdog for service: {service_to_monitor}")
#     watchdog(service_to_monitor, downtime_threshold, check_interval_seconds)
