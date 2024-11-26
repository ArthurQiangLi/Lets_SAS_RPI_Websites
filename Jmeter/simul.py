#!/usr/bin/env python3
import subprocess
import os
import time
from datetime import datetime, timedelta
import logging
import sys
import threading


# ----------------------- Configuration -----------------------

# Paths to JMeter executables and test plans
JMETER_PATH = "C:\\Utils\\apache-jmeter-5.6.3\\bin\\jmeter.bat"
REGULAR_TEST_PLAN = "C:\\Users\\danie\\Dropbox\\bonjr\\coding\\VSProjects\\Lets_SAS_RPI_Websites\\Jmeter\\traffic_simulation.jmx"
SPIKE_TEST_PLAN = "C:\\Users\\danie\\Dropbox\\bonjr\\coding\\VSProjects\\Lets_SAS_RPI_Websites\\Jmeter\\traffic_simulation_spike.jmx"

# Directories for storing results and logs
RESULTS_DIR = "C:\\Users\\danie\\Dropbox\\bonjr\\coding\\VSProjects\\Lets_SAS_RPI_Websites\\Jmeter\\jmeter_results"
LOG_DIR = "C:\\Users\\danie\\Dropbox\\bonjr\\coding\\VSProjects\\Lets_SAS_RPI_Websites\\Jmeter\\jmeter_logs"

# Total duration for automation (in days)
TOTAL_DURATION_DAYS = 3

# Interval between regular test runs (in seconds)
REGULAR_CHECK_INTERVAL_SECONDS = 300  # 5 minutes

# Spike configuration
SPIKE_DAY = 2  # Day to trigger spike (1-based index)
SPIKE_START_TIME = "12:00"  # 24-hour format, e.g., "14:30" for 2:30 PM
SPIKE_DURATION_SECONDS = 1800  # Duration to run spike test (e.g., 1800 seconds = 30 minutes)
SPIKE_TEST_PLAN_PATH = SPIKE_TEST_PLAN  # Path to spike test plan

# Retry configuration for failed test runs
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 60  # 1 minute

# Timestamp format for filenames
TIME_FORMAT = "%Y%m%d_%H%M%S"

# ------------------------------------------------------------

# ----------------------- Logging Setup -----------------------
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'jmeter_automation.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# ------------------------------------------------------------

# ----------------------- Helper Functions -----------------------

def run_jmeter_instance(test_plan, result_file, log_file):
    """
    Runs a single instance of JMeter in non-GUI mode.
    Returns True if successful, False otherwise.
    """
    command = [
        JMETER_PATH,
        "-n",
        "-t", test_plan,
        "-l", result_file,
        "-j", log_file
    ]

    logging.info(f"Starting JMeter test: {test_plan}")
    try:
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            stdout, stderr = proc.communicate()
            if proc.returncode == 0:
                logging.info(f"JMeter test completed successfully. Results saved to {result_file}")
                return True
            else:
                logging.error(f"JMeter test failed with return code {proc.returncode}")
                logging.error(f"Error Output: {stderr.decode('utf-8')}")
                return False
    except Exception as e:
        logging.error(f"Exception occurred while running JMeter: {e}")
        return False

def schedule_spike(start_datetime, spike_duration):
    """
    Schedules the spike test to run at a specified datetime for a given duration.
    """
    now = datetime.now()
    delay = (start_datetime - now).total_seconds()
    if delay < 0:
        logging.error("Spike start time is in the past. Cannot schedule spike.")
        return

    logging.info(f"Spike scheduled to start at {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    threading.Timer(delay, trigger_spike, [spike_duration]).start()

def trigger_spike(spike_duration):
    """
    Triggers the spike test and ensures it runs for the specified duration.
    """
    timestamp = datetime.now().strftime(TIME_FORMAT)
    result_file = os.path.join(RESULTS_DIR, f"test_results_spike_{timestamp}.jtl")
    log_file = os.path.join(LOG_DIR, f"jmeter_spike_log_{timestamp}.log")

    logging.info("Triggering spike JMeter test.")
    spike_thread = threading.Thread(target=run_jmeter_instance, args=(SPIKE_TEST_PLAN, result_file, log_file))
    spike_thread.start()

    # Allow the spike to run for the specified duration, then terminate if still running
    spike_thread.join(timeout=spike_duration)
    if spike_thread.is_alive():
        logging.warning("Spike test duration exceeded. Terminating spike JMeter process.")
        # Note: Terminating subprocesses gracefully requires additional handling.
        # For simplicity, we're not implementing it here.
    else:
        logging.info("Spike test completed within the expected duration.")

def manual_trigger_listener():
    """
    Listens for manual commands to trigger the spike test.
    """
    while True:
        user_input = input("Type 'trigger_spike' to manually trigger a spike test:\n")
        if user_input.strip().lower() == "trigger_spike":
            logging.info("Manual spike trigger command received.")
            trigger_spike(SPIKE_DURATION_SECONDS)
        else:
            print("Invalid command. Type 'trigger_spike' to trigger a spike.")

# ------------------------------------------------------------

# ----------------------- Main Function -----------------------

def main():
    """
    Main function to manage JMeter test runs over the specified duration.
    """
    start_time = datetime.now()
    end_time = start_time + timedelta(days=TOTAL_DURATION_DAYS)
    logging.info(f"JMeter automation started. Running for {TOTAL_DURATION_DAYS} days.")
    logging.info(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Determine the date for the spike (Day 2)
    spike_date = start_time + timedelta(days=SPIKE_DAY - 1)
    spike_datetime = datetime.strptime(spike_date.strftime('%Y-%m-%d') + ' ' + SPIKE_START_TIME, '%Y-%m-%d %H:%M')

    # Schedule the spike
    schedule_spike(spike_datetime, SPIKE_DURATION_SECONDS)

    # Initialize run count
    run_number = 1

    while datetime.now() < end_time:
        timestamp = datetime.now().strftime(TIME_FORMAT)
        result_file = os.path.join(RESULTS_DIR, f"test_results_regular_{timestamp}.jtl")
        log_file = os.path.join(LOG_DIR, f"jmeter_regular_log_{timestamp}.log")

        success = False
        retries = 0

        while not success and retries < MAX_RETRIES:
            success = run_jmeter_instance(REGULAR_TEST_PLAN, result_file, log_file)
            if not success:
                retries += 1
                logging.warning(f"Retrying JMeter test ({retries}/{MAX_RETRIES}) after {RETRY_DELAY_SECONDS} seconds...")
                time.sleep(RETRY_DELAY_SECONDS)

        if not success:
            logging.error(f"JMeter test failed after {MAX_RETRIES} retries. Exiting automation.")
            sys.exit("JMeter test failed. Check logs for details.")

        logging.info(f"Regular JMeter run {run_number} completed.")
        run_number += 1

        # Calculate time to next run
        next_run_time = datetime.now() + timedelta(seconds=REGULAR_CHECK_INTERVAL_SECONDS)
        sleep_duration = (next_run_time - datetime.now()).total_seconds()
        if sleep_duration > 0:
            logging.info(f"Sleeping for {int(sleep_duration)} seconds before next regular run.")
            time.sleep(sleep_duration)

    logging.info("JMeter automation completed successfully.")

# ------------------------------------------------------------

if __name__ == "__main__":
    # Create results and logs directories if they don't exist
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    # Check for command-line argument
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "manual_spike":
            logging.info("Manual spike triggered via command line.")
            trigger_spike(SPIKE_DURATION_SECONDS)
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("Usage:")
            print("  python simul.py          # Run the full automation")
            print("  python simul.py manual_spike  # Trigger a manual spike")
    else:
        # Start the automation
        main()
