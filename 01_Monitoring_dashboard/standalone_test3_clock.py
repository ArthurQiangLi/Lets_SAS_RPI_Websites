import os

def get_arm_clock():
    try:
        output = os.popen("vcgencmd measure_clock arm").readline()
        return int(output.split("=")[1]) // 1_000_000  # Convert Hz to MHz
    except Exception as e:
        return f"Error: {e}"

def get_apache_status():
    try:
        result = os.popen("systemctl is-active apache2").readline()
        return result.strip()=="active"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    arm_clock = get_arm_clock() # int 600 = 600Mhz
    apache_status = get_apache_status() # bool, true=active, false=stopped
    
    print(f"Apache Server Status: {apache_status}")
    print(f"ARM CPU Clock: {arm_clock} MHz")
