# Read temperature of RPI

## 1. In command line

| Methods                | Howto                                                                                                                                                                                                             |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Using `vcgencmd`       | use <br> `vcgencmd measure_temp` <br> output: <br>`temp=45.3'C`                                                                                                                                                   |
| Read from `/sys` files | use <br> `cat /sys/class/thermal/thermal_zone0/temp` <br> will return: `45333` in 0.001 degrees Celsius. <br> use <br>`awk '{print $1/1000}' /sys/class/thermal/thermal_zone0/temp` to convert to degree Celsius. |

## 2. In Python

### using `vcgencmd`

```py
import os

def get_temperature_vcgencmd():
    try:
        # Run the vcgencmd command and read the output
        temp_output = os.popen("vcgencmd measure_temp").readline()
        if temp_output:
            # Extract the temperature value
            temperature = temp_output.replace("temp=", "").replace("'C\n", "").strip()
            return float(temperature)
        else:
            return None
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

# Example usage
temperature = get_temperature_vcgencmd()
print(f"Temperature (vcgencmd): {temperature}°C")


```

### using `/sys/`

```py
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
temperature = get_temperature_sys()
print(f"Temperature (/sys): {temperature}°C")

```
