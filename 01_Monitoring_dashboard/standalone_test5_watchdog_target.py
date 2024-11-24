import os
import subprocess

def is_pid_running(pid_file):
    """Check if the process in the PID file is running."""
    try:
        if os.path.exists(pid_file):
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())
            # Check if the process exists
            return os.path.exists(f"/proc/{pid}")
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def is_service_active(service_name):
    """Check if the service is active using systemctl."""
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            stdout=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip() == "active"
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    pid_file = "/var/run/apache2/apache2.pid"
    service_name = "apache2"

    # Check using PID file
    if is_pid_running(pid_file):
        print("Apache process is running (based on PID file).")
    else:
        print("Apache process is not running (based on PID file).")

    # Check using systemctl
    if is_service_active(service_name):
        print("Apache service is active (based on systemctl).")
    else:
        print("Apache service is not active (based on systemctl).")