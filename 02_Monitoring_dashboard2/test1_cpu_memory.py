import psutil
import logging

def calculate_memory_usage(use_total_memory=False):
    try:
        memory = psutil.virtual_memory()
        if use_total_memory:
            return memory.percent
        else:
            actual_memory_percent = 100 * (memory.used - memory.buffers - memory.cached) / memory.total
            return actual_memory_percent
    except Exception as e:
        logging.error(f"Error calculating memory usage: {e}")
        return 0  # Return 0 if unable to calculate

def get_cpu_usage(interval=1):
    try:
        return psutil.cpu_percent(interval=interval)
    except Exception as e:
        logging.error(f"Error fetching CPU usage: {e}")
        return 0
