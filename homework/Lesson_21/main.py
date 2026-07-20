import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_coordinates(city):
    params = {
        "name": city,
        "count": 1
    }

    try:
        response = requests.get(GEOCODING_URL, params=params)
        response.raise_for_status()

        data = response.json()

        if "results" not in data:
            return None

        result = data["results"][0]

        return {
            "name": result["name"],
            "latitude": result["latitude"],
            "longitude": result["longitude"]
        }

    except requests.exceptions.RequestException:
        print("Failed to connect to Geocoding API.")
        return None


def get_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto"
    }

    try:
        response = requests.get(WEATHER_URL, params=params)
        response.raise_for_status()

        data = response.json()

        return data["current"]

    except requests.exceptions.RequestException:
        print("Failed to connect to Weather API.")
        return None


def main():
    city = input("Enter city name: ")

    location = get_coordinates(city)

    if location is None:
        print("City not found")
        return

    weather = get_weather(
        location["latitude"],
        location["longitude"]
    )

    if weather is None:
        return

    print(f"City: {location['name']}")
    print(f"Temperature: {weather['temperature_2m']} °C")
    print(f"Wind Speed: {weather['wind_speed_10m']} km/h")
    print(f"Time: {weather['time']}")


if __name__ == "__main__":
    main()