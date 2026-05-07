import httpx
from typing import Any

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WMO_CODES: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}


class WeatherService:
    """Handles geocoding and weather data fetching from Open-Meteo."""

    async def _geocode(self, location: str) -> tuple[float, float, str]:
        """
        Resolve a location name to latitude/longitude.

        Args:
            location: City or place name.

        Returns:
            Tuple of (latitude, longitude, resolved_name).

        Raises:
            ValueError: If the location cannot be found.
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                GEOCODING_URL,
                params={"name": location, "count": 1, "language": "en", "format": "json"},
            )
            response.raise_for_status()
            data = response.json()

        results = data.get("results")
        if not results:
            raise ValueError(f"Location not found: '{location}'. Please try a different city name.")

        result = results[0]
        name = f"{result['name']}, {result.get('country', '')}".strip(", ")
        return result["latitude"], result["longitude"], name

    def _describe_condition(self, wmo_code: int) -> str:
        """Map a WMO weather code to a human-readable description."""
        return WMO_CODES.get(wmo_code, f"Unknown condition (code {wmo_code})")

    async def get_current_weather(self, location: str) -> str:
        """
        Fetch current weather conditions for a location.

        Args:
            location: City or place name.

        Returns:
            Formatted string of current conditions.
        """
        lat, lon, resolved_name = await self._geocode(location)

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                WEATHER_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
                    "timezone": "auto",
                },
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()

        current = data["current"]
        condition = self._describe_condition(current["weather_code"])

        return (
            f"Current weather in {resolved_name}:\n"
            f"  Condition:    {condition}\n"
            f"  Temperature:  {current['temperature_2m']}°C\n"
            f"  Humidity:     {current['relative_humidity_2m']}%\n"
            f"  Wind speed:   {current['wind_speed_10m']} km/h"
        )

    async def get_forecast(self, location: str, days: int = 3) -> str:
        """
        Fetch a daily weather forecast for a location.

        Args:
            location: City or place name.
            days: Number of forecast days (1-7).

        Returns:
            Formatted string of daily forecast.
        """
        if not 1 <= days <= 7:
            raise ValueError(f"Days must be between 1 and 7, got {days}.")

        lat, lon, resolved_name = await self._geocode(location)

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                WEATHER_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
                    "forecast_days": days,
                    "timezone": "auto",
                },
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()

        daily = data["daily"]
        lines = [f"{days}-day forecast for {resolved_name}:\n"]

        for i in range(days):
            date = daily["time"][i]
            high = daily["temperature_2m_max"][i]
            low = daily["temperature_2m_min"][i]
            precip = daily["precipitation_probability_max"][i]
            condition = self._describe_condition(daily["weather_code"][i])
            lines.append(
                f"  {date}: {condition}, High {high}°C / Low {low}°C, "
                f"Precipitation chance: {precip}%"
            )

        return "\n".join(lines)