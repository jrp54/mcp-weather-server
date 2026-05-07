import asyncio
from mcp.server.fastmcp import FastMCP
from place import PlaceService

# Initialize FastMCP server
mcp = FastMCP("PlaceServer")
place_service = PlaceService()

@mcp.tool()
async def get_timezone(location: str) -> str:
    """
    Get the local timezone for a specific location.
    
    Args:
        location: The name of the city or place.
    """
    try:
        return await place_service.get_timezone(location)
    except Exception as e:
        return f"Error fetching timezone: {str(e)}"

@mcp.tool()
async def get_air_quality(location: str) -> str:
    """
    Get the current Air Quality Index (AQI) and pollutant levels.
    """
    try:
        return await place_service.get_air_quality(location)
    except Exception as e:
        return f"Error fetching air quality: {str(e)}"

@mcp.tool()
async def get_astronomy(location: str) -> str:
    """
    Get the sunrise and sunset times for a location.
    """
    try:
        return await place_service.get_astronomy(location)
    except Exception as e:
        return f"Error fetching astronomy data: {str(e)}"

@mcp.tool()
async def get_current_weather(location: str) -> str:
    """
    Get real-time current weather conditions for a specific location.
    
    Args:
        location: The name of the city or place (e.g., 'London', 'Tokyo').
    """
    try:
        return await place_service.get_current_weather(location)
    except Exception as e:
        return f"Error fetching current weather: {str(e)}"

@mcp.tool()
async def get_forecast(location: str, days: int = 3) -> str:
    """
    Get a multi-day weather forecast for a specific location.
    
    Args:
        location: The name of the city or place.
        days: Number of days to forecast (1-7). Default is 3.
    """
    try:
        return await place_service.get_forecast(location, days)
    except Exception as e:
        return f"Error fetching forecast: {str(e)}"

@mcp.tool()
async def get_place_summary(location: str) -> str:
    """
    Get a comprehensive summary of a place: weather, timezone, AQI, and astronomy.
    Perfect for providing a quick overview to a user.
    
    Args:
        location: The name of the city or place.
    """
    try:
        tz = await place_service.get_timezone(location)
        current = await place_service.get_current_weather(location)
        aqi = await place_service.get_air_quality(location)
        astro = await place_service.get_astronomy(location)
        forecast = await place_service.get_forecast(location, days=2)
        return f"--- PLACE INTELLIGENCE: {location} ---\n{tz}\n\n{current}\n\n{aqi}\n\n{astro}\n\n--- SHORT-TERM LOOK ---\n{forecast}"
    except Exception as e:
        return f"Error generating place summary: {str(e)}"

if __name__ == "__main__":
    # FastMCP handles the stdio transport automatically when run as a script
    # This is the standard entry point for Claude Desktop and other clients.
    mcp.run()
