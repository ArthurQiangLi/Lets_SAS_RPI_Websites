# you need to run as " sudo python standalone.py "

def set_cpu_frequency(frequency_khz):
    try:
        path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_setspeed"
        with open(path, "w") as f:
            f.write(str(frequency_khz))
        print(f"CPU frequency set to {frequency_khz / 1000} MHz")
    except PermissionError:
        print("Permission denied. Run the script with sudo.")
    except Exception as e:
        print(f"Error: {e}")

def set_governor(governor):
    try:
        path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
        with open(path, "w") as f:
            f.write(governor)
        print(f"Governor set to {governor}")
    except PermissionError:
        print("Permission denied. Run the script with sudo.")
    except Exception as e:
        print(f"Error: {e}")

def get_cpu_frequency():
    try:
        path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
        with open(path, "r") as f:
            freq = int(f.read().strip())
        print(f"Current CPU frequency: {freq / 1000} MHz")
    except Exception as e:
        print(f"Error: {e}")

#######################################################################

import os

def set_cpu_frequency2(frequency_khz):
    try:
        # Use sudo to write the frequency to scaling_setspeed
        os.system(f"echo {frequency_khz} | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_setspeed > /dev/null")
        print(f"CPU frequency set to {frequency_khz / 1000} MHz")
    except Exception as e:
        print(f"Error setting CPU frequency: {e}")

def set_governor2(governor):
    try:
        # Use sudo to write the governor to scaling_governor
        os.system(f"echo {governor} | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor > /dev/null")
        print(f"Governor set to {governor}")
    except Exception as e:
        print(f"Error setting governor: {e}")

def get_cpu_frequency2():
    try:
        # Read the current CPU frequency from scaling_cur_freq
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r") as f:
            freq = int(f.read().strip())
        print(f"Current CPU frequency: {freq / 1000} MHz")
    except Exception as e:
        print(f"Error reading CPU frequency: {e}")


if __name__ == "__main__":
    if (False):
        get_cpu_frequency()
        set_cpu_frequency(1200000)# Set a specific CPU frequency (e.g., 1.2 GHz = 1200000 kHz)

        set_governor("performance") # Set the CPU governor to "performance"

        get_cpu_frequency()
    else:
        get_cpu_frequency()

        set_cpu_frequency2(1200000)# Set a specific CPU frequency (e.g., 1.2 GHz = 1200000 kHz)

        set_governor2("performance")# Set the CPU governor to "performance"

        get_cpu_frequency()# Get and print the current CPU frequency