# MCP Place Intelligence Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that provides real-time "place intelligence" — including weather, timezones, air quality, and astronomy data — via the [Open-Meteo API](https://open-meteo.com/). No API key required.

## What is MCP?

The Model Context Protocol is an open standard that lets LLMs call out to external tools and data sources at runtime. Instead of relying on training data, a connected LLM can invoke tools on this server to fetch live, accurate information — like the current temperature in Tokyo or a 7-day forecast for London.

## Features

- No API keys or accounts required
- Current conditions: temperature, humidity, wind speed, weather description
- Environmental data: Air Quality Index (AQI) and UV Index
- Astronomical data: Sunrise and sunset times
- Daily forecast up to 7 days
- Timezone lookup for any city
- Natural language "place summaries" designed for LLM responses
- Fully async with `httpx`, type-hinted throughout
- Works with Claude Desktop, MCP Inspector, or any MCP-compatible client

## Setup

**Prerequisites:** Python 3.11+, Node.js (for MCP Inspector)

```bash
git clone https://github.com/jrp54/mcp-place-intelligence-server.git
cd mcp-place-intelligence-server

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Testing with MCP Inspector

The easiest way to verify the server is working without a full LLM client:

```bash
source .venv/bin/activate
npx @modelcontextprotocol/inspector python server.py
```

Open the URL shown in your terminal, click **Connect**, then navigate to the **Tools** tab to call any tool manually.

## Connecting to Claude Desktop

Find your config file:

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows (direct install) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Windows (Microsoft Store) | `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json` |
| WSL | Use the Windows path above — Claude Desktop runs on the Windows side |

Add the following to your config (merge with any existing content):

**Standard:**
```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-weather-server/server.py"]
    }
  }
}
```

**From WSL** (Claude Desktop on Windows, server in WSL):
```json
{
  "mcpServers": {
    "place-intelligence": {
      "command": "wsl",
      "args": [
        "-e",
        "/home/yourusername/path/to/mcp-place-intelligence-server/.venv/bin/python",
        "/home/yourusername/path/to/mcp-place-intelligence-server/server.py"
      ]
    }
  }
}
```

Fully quit and relaunch Claude Desktop. A hammer icon near the chat input confirms the server connected successfully.

> **Note:** Claude Desktop has a built-in weather widget that may respond to generic weather questions. To explicitly invoke this MCP server, ask Claude to *"use the weather MCP tool"* or reference a tool by name (e.g. *"use get_weather_summary for Berlin"*).
> **Note:** Claude Desktop has a built-in weather widget that may respond to generic weather questions. To explicitly invoke this MCP server, ask Claude to *"use the place intelligence MCP tool"* or reference a tool by name (e.g. *"use get_place_summary for Berlin"*).

## Tools

### `get_timezone(location)`
Returns the local timezone for a city (e.g., "Europe/Berlin").

### `get_air_quality(location)`
Returns current AQI (US and EU standards) and pollutant levels (PM2.5, PM10).

### `get_astronomy(location)`
Returns today's sunrise and sunset times for the location.

### `get_current_weather(location)`
Returns current temperature, humidity, wind speed, and UV index.

### `get_forecast(location, days?)`
Returns a daily forecast for 1–7 days (default: 3). Includes high/low temps and precipitation probability.

### `get_place_summary(location)`
Returns a comprehensive overview of a location, combining timezone, weather, air quality, and astronomy into one response.

## Credits

- Weather & geocoding data: [Open-Meteo](https://open-meteo.com/)
- Protocol: [Model Context Protocol](https://modelcontextprotocol.io/)
- Server framework: [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)