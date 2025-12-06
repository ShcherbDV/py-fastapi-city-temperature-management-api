import httpx
from fastapi import HTTPException


async def fetch_temperature_for_city(city_name: str) -> float:

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"

    async with httpx.AsyncClient() as client:
        geo_response = await client.get(geo_url)

    if geo_response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Geocoding API returned: {geo_response.text}"
        )

    try:
        geo_data = geo_response.json()
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail=f"Geocoding API returned invalid JSON: {geo_response.text}"
        )

    if "results" not in geo_data:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city_name}' not found in geocoding API"
        )

    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]

    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    async with httpx.AsyncClient() as client:
        weather_response = await client.get(weather_url)

    if weather_response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Weather API error: {weather_response.text}"
        )

    try:
        weather_data = weather_response.json()
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail=f"Weather API returned invalid JSON: {weather_response.text}"
        )

    if "current_weather" not in weather_data:
        raise HTTPException(
            status_code=500,
            detail=f"Weather API JSON missing 'current_weather': {weather_data}"
        )

    return weather_data["current_weather"]["temperature"]
