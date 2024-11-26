import psutil
import os

def extern_get_cpu_memory_usage():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent
    }


def extern_get_arm_clock():
    try:
        output = os.popen("vcgencmd measure_clock arm").readline()
        return int(output.split("=")[1]) // 1_000_000  # Convert Hz to MHz
    except Exception as e:
        return 0 #f"Error: {e}"

def extern_get_apache_active():
    try:
        result = os.popen("systemctl is-active apache2").readline()
        return result.strip()=="active"
    except Exception as e:
        return f"Error: {e}"

def extern_get_pi_throttled_status():
    try:
        output = os.popen("vcgencmd get_throttled").readline()
        
        # Extract the throttled value
        if "throttled=" in output:
            throttled_hex = output.split("=")[1]
            throttled_int = int(throttled_hex, 16)  # Convert hex to int
        else:
            raise ValueError("###Unexpected output format from vcgencmd, make sure it's on a RPi first.")

        # Parse the throttled value into variables
        under_voltage = bool(throttled_int & 0x1)          # Bit 0
        currently_throttled = bool(throttled_int & 0x2)    # Bit 1
        freq_capped = bool(throttled_int & 0x4)            # Bit 2
        under_voltage_occurred = bool(throttled_int & 0x10000)  # Bit 16
        throttling_occurred = bool(throttled_int & 0x20000)     # Bit 17
        freq_capped_occurred = bool(throttled_int & 0x40000)    # Bit 18

        # Return the results in a dictionary
        return {
            "under_voltage": under_voltage,
            "currently_throttled": currently_throttled,
            "freq_capped": freq_capped,
            "under_voltage_occurred": under_voltage_occurred,
            "throttling_occurred": throttling_occurred,
            "freq_capped_occurred": freq_capped_occurred
        }
    except Exception as e:
        print(f"Error parsing throttled status: {e}")
        return None
    
# How to use?
# if __name__ == "__main__":
#     arm_clock = extern_get_arm_clock() #return int 600, means 600Mhz
#     apache_status = extern_get_apache_active() # bool, true=active, false=stopped
    
#     print(f"Apache Server Status: {apache_status}")
#     print(f"ARM CPU Clock: {arm_clock} MHz")

# if __name__ == "__main__":
#     status = extern_get_pi_throttled_status() #return a boolean dictionary {"under_voltage": True, ...}
#     print(status) #as a dictionary
#     if status:
#         print("Throttling Status:")
#         print(f"Under-voltage detected: {status['under_voltage']}")
#         print(f"Currently throttled: {status['currently_throttled']}")
#         print(f"Frequency capped: {status['freq_capped']}")
#         print(f"Under-voltage occurred since boot: {status['under_voltage_occurred']}")
#         print(f"Throttling occurred since boot: {status['throttling_occurred']}")
#         print(f"Frequency capping occurred since boot: {status['freq_capped_occurred']}")