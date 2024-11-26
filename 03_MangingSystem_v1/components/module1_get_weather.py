


import requests
import logging

WEATHER_API_KEY = "7a8fdd951ab780e11ad83ac773f07e7f"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
LOCATION = "Kitchener,CA"

def extern_get_weather(city):
    return "-99°C, Clear Skies"

def extern_fetch_weather():
    try:
        response = requests.get(WEATHER_API_URL, params={
            "q": LOCATION,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }, timeout=5)
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            weather = data['weather'][0]['description']
            return {"temp":temp, "humidity": humidity, "weather":weather}
        else:
            logging.error(f"Weather API Error: {data.get('message', 'Unknown error')}")
            return {"temp":None, "humidity": None, "weather":None}
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return {"temp":None, "humidity": None, "weather":None}

#usage
# weather = extern_fetch_weather() #return {"temp":-3, "humidity": 98, "weather":mist}