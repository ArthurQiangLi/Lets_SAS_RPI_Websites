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


if __name__ == "__main__":
    # Set a specific CPU frequency (e.g., 1.2 GHz = 1200000 kHz)
    set_cpu_frequency(1200000)

    # Set the CPU governor to "performance"
    set_governor("performance")

    get_cpu_frequency()