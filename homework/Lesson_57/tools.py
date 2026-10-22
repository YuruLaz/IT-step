import requests
from langchain_core.tools import tool

from data import HOTELS, ATTRACTIONS

EXCHANGE_RATE_API_URL = "https://open.er-api.com/v6/latest/{currency}"
WEATHER_API_URL = "https://wttr.in/{city}?format=j1"


@tool
def search_hotel(city: str) -> str:
    """Search for available hotels in a given city, with price per night in GEL."""
    hotels = HOTELS.get(city.lower())
    if not hotels:
        return f"No hotels found for {city}."

    return "\n".join(f"- {name} - {price} GEL/night" for name, price in hotels)
    # - Hotel A - 120 GEL/night
    # - Hotel B - 180 GEL/night
    # - Hotel C - 250 GEL/night


@tool
def get_exchange_rate(currency: str) -> str:
    """Get the current exchange rate of a currency (e.g. USD, EUR, GBP) to GEL, fetched live."""
    currency = currency.upper()
    try:
        response = requests.get(EXCHANGE_RATE_API_URL.format(currency=currency), timeout=5)
        response.raise_for_status()
        data = response.json()
    #cant get exchange rate
    except requests.RequestException:
        return f"Could not fetch exchange rate for {currency} right now."

    #200 but no GEL rate
    if data.get("result") != "success":
        return f"No exchange rate found for {currency}."

    rate = data["rates"].get("GEL")
    if rate is None:
        return f"No GEL rate available for {currency}."

    return f"{currency} = {rate:.2f} GEL"
    # USD = 2.60 GEL


@tool
def get_weather(city: str) -> str:
    """Get the current weather forecast for a given city."""

    try:
        response = requests.get(WEATHER_API_URL.format(city=city), timeout=5)
        response.raise_for_status()
        data = response.json()
    #cant get city weather
    except requests.RequestException:
        return f"Could not fetch weather data for {city} right now."

    return f"Weather in {city}: {data['current_condition'][0]['temp_C']}°C"
    # Weather in Tbilisi: 18°C


@tool
def search_attractions(city: str) -> str:
    """Search for popular tourist attractions in a given city."""
    attractions = ATTRACTIONS.get(city.lower())
    if not attractions:
        return f"No attractions found for {city}."

    return f"\n{city}:\n" + "".join(f"-{attraction}\n" for attraction in attractions)
    # Tbilisi:
    # -Narikala Fortress
    # -Old Tbilisi
    # -Mtatsminda Park
