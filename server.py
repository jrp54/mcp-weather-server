import asyncio
from mcp.server.fastmcp import FastMCP
from weather import WeatherService

# Initialize FastMCP server
mcp = FastMCP("WeatherServer")
weather_service = WeatherService()

@mcp.tool()
async def get_current_weather(location: str) -> str:
    """
    Get real-time current weather conditions for a specific location.
    
    Args:
        location: The name of the city or place (e.g., 'London', 'Tokyo').
    """
    try:
        return await weather_service.get_current_weather(location)
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
        return await weather_service.get_forecast(location, days)
    except Exception as e:
        return f"Error fetching forecast: {str(e)}"

@mcp.tool()
async def get_weather_summary(location: str) -> str:
    """
    Get a natural language summary combining current weather and a 2-day forecast.
    Perfect for providing a quick overview to a user.
    
    Args:
        location: The name of the city or place.
    """
    try:
        current = await weather_service.get_current_weather(location)
        forecast = await weather_service.get_forecast(location, days=2)
        return f"--- WEATHER SUMMARY ---\n{current}\n\n--- SHORT-TERM LOOK ---\n{forecast}"
    except Exception as e:
        return f"Error generating weather summary: {str(e)}"

if __name__ == "__main__":
    # FastMCP handles the stdio transport automatically when run as a script
    # This is the standard entry point for Claude Desktop and other clients.
    mcp.run()
