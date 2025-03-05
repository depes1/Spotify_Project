import requests
import os
import json
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# OpenWeather API endpoint
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(lat, lon):
    """Fetches current weather data for a given coordinates."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"API Call Failed: {response.status_code}, {response.text}")

if __name__ == "__main__":
    
    # Getting Maringá coordinates
    lat = -23.4210
    lon = -51.9331

    try:
        weather_data = get_weather(lat, lon)

        # Extracting relevant information
        parsed_data = {
            "city": weather_data["name"],
            "weather_main": weather_data["weather"][0]["main"],
            "weather_description": weather_data["weather"][0]["description"],
            "current_temp_celsius": weather_data["main"]["temp"],
            "humidity_pct": weather_data["main"]["humidity"],
            "wind_speed_ms": weather_data["wind"]["speed"],
            "clouds_all": weather_data["clouds"]["all"]
        }

        print(json.dumps(parsed_data, indent=4))

        # Save to JSON file
        with open("weather.json", "w") as file:
            json.dump(parsed_data, file, indent=4)

    except Exception as e:
        print(f"Error: {e}")
