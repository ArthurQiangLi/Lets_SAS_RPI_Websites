import json
from datetime import datetime

def extern_get_age(json_file_path = "config.json"):
    # Load the birthday from the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        birthday_str = data.get("birthday")
    
    if not birthday_str:
        raise ValueError("Birthday not found in the JSON file.")
    
    # Convert the birthday string to a datetime object
    birthday = datetime.strptime(birthday_str, "%Y-%m-%d %H:%M:%S")
    
    # Get the current time
    now = datetime.now()
    
    # Calculate the age difference
    delta = now - birthday
    
    # Extract days, hours, minutes, and seconds
    days = delta.days
    seconds_in_day = delta.seconds
    hours = seconds_in_day // 3600
    minutes = (seconds_in_day % 3600) // 60
    seconds = (seconds_in_day % 3600) % 60
    
    # Return formatted age string
    return f"{days} d, {hours} h, {minutes} m, {seconds} s"