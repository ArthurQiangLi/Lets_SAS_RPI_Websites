import os

def extern_get_cpu_temperature1():
    try:
        # Get the temperature using the vcgencmd command
        temp_output = os.popen("vcgencmd measure_temp").readline()
        if temp_output:
            # Extract the temperature value
            temperature = temp_output.replace("temp=", "").replace("'C\n", "").strip()
            return float(temperature)
        else:
            return "Unable to read temperature. Note 'vcgencmd' might only work on a Pi."
    except Exception as e:
        return f"Error: {e}"

def get_temperature_sys():
    try:
        # Read the temperature value from the file
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
            temp_raw = file.read().strip()
            # Convert from millidegrees Celsius to degrees Celsius
            temperature = int(temp_raw) / 1000.0
            return round(temperature, 1)  # Optional: Round to 1 decimal place
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

# Example usage



# if __name__ == "__main__":
#     temperature = extern_get_cpu_temperature1()
#     print(f"#### Temperature(vcgencmd): {temperature}°C")
#     temperature = get_temperature_sys()
#     print(f"#### Temperature (/sys): {temperature}°C")