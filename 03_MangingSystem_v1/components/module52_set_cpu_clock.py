import os

def extern_set_cpu_frequency2(frequency_khz):
    try:
        # Use sudo to write the frequency to scaling_setspeed
        os.system(f"echo {frequency_khz} | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_setspeed > /dev/null")
        print(f"CPU frequency set to {frequency_khz / 1000} MHz")
    except Exception as e:
        print(f"Error setting CPU frequency: {e}")

#    - **`performance`**: Runs at the **maximum** frequency.
#    - **`powersave`**: Runs at the **minimum** frequency.
#    - **`ondemand`**: Dynamically adjusts based on CPU load.
def extern_set_governor2(governor):
    try:
        # Use sudo to write the governor to scaling_governor
        os.system(f"echo {governor} | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor > /dev/null")
        print(f"Governor set to {governor}")
    except Exception as e:
        print(f"Error setting governor: {e}")


#usage
# get_cpu_frequency()

# set_cpu_frequency2(1200000)# Set a specific CPU frequency (e.g., 1.2 GHz = 1200000 kHz)

# set_governor2("performance")# Set the CPU governor to "performance"

# get_cpu_frequency()# Get and print the current CPU frequency