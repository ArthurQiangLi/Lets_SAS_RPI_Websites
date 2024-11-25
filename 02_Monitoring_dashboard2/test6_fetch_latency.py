import os
import logging

ACCESS_LOG_FILE = "/var/log/apache2/access.log"

def get_average_latency(n=100):
    try:
        lines_to_read = n
        block_size = 8192
        data = bytearray()
        lines = []
        latencies = []

        with open(ACCESS_LOG_FILE, 'rb') as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            remaining_size = file_size

            while len(lines) < lines_to_read and remaining_size > 0:
                read_size = min(block_size, remaining_size)
                f.seek(remaining_size - read_size)
                buffer = f.read(read_size)
                data = buffer + data
                remaining_size -= read_size
                lines = data.split(b'\n')

            lines = [line.decode('utf-8', errors='ignore') for line in lines if line.strip()]
            target_lines = [line for line in reversed(lines) if 'python-requests' not in line]

            if not target_lines:
                logging.warning("No valid lines found in the log.")
                return None

            for line in target_lines[:n]:
                try:
                    latency_str = line.split()[-1]
                    latency = float(latency_str)
                    latencies.append(latency)
                except (IndexError, ValueError):
                    continue

            if not latencies:
                logging.warning("No valid latency values found.")
                return None

            average_latency = sum(latencies) / len(latencies)
            return average_latency / 1000

    except Exception as e:
        logging.error(f"Error reading latency from access log: {e}")
        return None
