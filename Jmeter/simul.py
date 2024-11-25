#!/usr/bin/env python3
import subprocess
import os
import time
from datetime import datetime, timedelta
import logging
import sys

# Configuration
JMETER_PATH = "/mnt/c/Utils/apache-jmeter-5.6.3/bin/jmeter"
TEST_PLAN = "/mnt/c/Users/danie/Dropbox/bonjr/coding/VSProjects/Lets_SAS_RPI_Websites/Jmeter/traffic_simulation.jmx" 
RESULTS_DIR = "/mnt/c/Users/danie/Dropbox/bonjr/coding/VSProjects/Lets_SAS_RPI_Websites/Jmeter/jmeter_results"
LOG_DIR = "/mnt/c/Users/danie/Dropbox/bonjr/coding/VSProjects/Lets_SAS_RPI_Websites/Jmeter/jmeter_logs"
TOTAL_DURATION_DAYS = 3
CHECK_INTERVAL_SECONDS = 300  # Check every 5 minutes
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 60  # Wait 1 minute before retrying
TIME_FORMAT = "%Y%m%d_%H%M%S"

# Setup Logging
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'jmeter_automation.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Ensure JMeter executable exists
if not os.path.isfile(JMETER_PATH):
    logging.error(f"JMeter executable not found at {JMETER_PATH}")
    sys.exit(f"JMeter executable not found at {JMETER_PATH}")

# Create results directory if it doesn't exist
os.makedirs(RESULTS_DIR, exist_ok=True)

def run_jmeter_instance(test_plan, result_file, log_file):
    """
    Runs a single instance of JMeter in non-GUI mode.
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

def main():
    """
    Main function to manage JMeter test runs over the specified duration.
    """
    start_time = datetime.now()
    end_time = start_time + timedelta(days=TOTAL_DURATION_DAYS)
    logging.info(f"JMeter automation started. Running for {TOTAL_DURATION_DAYS} days.")
    logging.info(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    while datetime.now() < end_time:
        timestamp = datetime.now().strftime(TIME_FORMAT)
        result_file = os.path.join(RESULTS_DIR, f"test_results_{timestamp}.jtl")
        log_file = os.path.join(LOG_DIR, f"jmeter_log_{timestamp}.log")

        success = False
        retries = 0

        while not success and retries < MAX_RETRIES:
            success = run_jmeter_instance(TEST_PLAN, result_file, log_file)
            if not success:
                retries += 1
                logging.warning(f"Retrying JMeter test ({retries}/{MAX_RETRIES}) after {RETRY_DELAY_SECONDS} seconds...")
                time.sleep(RETRY_DELAY_SECONDS)

        if not success:
            logging.error(f"JMeter test failed after {MAX_RETRIES} retries. Exiting automation.")
            sys.exit("JMeter test failed. Check logs for details.")

        # Calculate time to next check
        next_run_time = datetime.now() + timedelta(seconds=CHECK_INTERVAL_SECONDS)
        sleep_duration = (next_run_time - datetime.now()).total_seconds()
        if sleep_duration > 0:
            logging.info(f"Sleeping for {int(sleep_duration)} seconds before next run.")
            time.sleep(sleep_duration)

    logging.info("JMeter automation completed successfully.")

if __name__ == "__main__":
    main()
