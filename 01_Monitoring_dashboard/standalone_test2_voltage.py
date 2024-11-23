import os

def get_parse_throttled_status():
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

# Example usage
if __name__ == "__main__":
    status = get_parse_throttled_status()
    if status:
        print("Throttling Status:")
        print(f"Under-voltage detected: {status['under_voltage']}")
        print(f"Currently throttled: {status['currently_throttled']}")
        print(f"Frequency capped: {status['freq_capped']}")
        print(f"Under-voltage occurred since boot: {status['under_voltage_occurred']}")
        print(f"Throttling occurred since boot: {status['throttling_occurred']}")
        print(f"Frequency capping occurred since boot: {status['freq_capped_occurred']}")
