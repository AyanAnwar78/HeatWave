"""
Open-Meteo API service layer for HeatGuard.

Docs: https://open-meteo.com/en/docs
Geocoding: https://open-meteo.com/en/docs/geocoding-api
"""

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL  = "https://api.open-meteo.com/v1/forecast"

CURRENT_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "weather_code",
    "wind_speed_10m",
    "wind_direction_10m",
    "precipitation",
    "uv_index",
    "cloud_cover",
]

HOURLY_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "weather_code",
    "precipitation_probability",
    "wind_speed_10m",
]

DAILY_VARS = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "apparent_temperature_max",
    "precipitation_sum",
    "wind_speed_10m_max",
    "uv_index_max",
    "sunrise",
    "sunset",
]

WMO_CODES = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Icy Fog", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Moderate Drizzle", "🌦️"),
    55: ("Dense Drizzle", "🌧️"),
    61: ("Slight Rain", "🌧️"),
    63: ("Moderate Rain", "🌧️"),
    65: ("Heavy Rain", "🌧️"),
    71: ("Slight Snow", "🌨️"),
    73: ("Moderate Snow", "🌨️"),
    75: ("Heavy Snow", "❄️"),
    80: ("Rain Showers", "🌦️"),
    81: ("Moderate Showers", "🌦️"),
    82: ("Violent Showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm w/ Hail", "⛈️"),
    99: ("Thunderstorm w/ Heavy Hail", "⛈️"),
}


def get_wmo_description(code: int):
    return WMO_CODES.get(code, ("Unknown", "🌡️"))


def geocode_city(city: str) -> dict | None:
    """Return geocoding result for a city name, or None on failure."""
    try:
        resp = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if not results:
            return None
        r = results[0]
        return {
            "name": r.get("name", city),
            "country": r.get("country_code", ""),
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "timezone": r.get("timezone", "UTC"),
        }
    except Exception:
        return None


def fetch_weather(latitude: float, longitude: float, timezone: str = "auto") -> dict | None:
    """Fetch current, hourly, and daily weather from Open-Meteo."""
    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(CURRENT_VARS),
            "hourly": ",".join(HOURLY_VARS),
            "daily": ",".join(DAILY_VARS),
            "timezone": timezone,
            "forecast_days": 7,
            "wind_speed_unit": "kmh",
        }
        resp = requests.get(FORECAST_URL, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def parse_current(data: dict) -> dict:
    """Extract and label current weather fields from API response."""
    c = data.get("current", {})
    code = c.get("weather_code", 0)
    desc, emoji = get_wmo_description(code)
    return {
        "temperature":   round(c.get("temperature_2m", 0), 1),
        "humidity":      round(c.get("relative_humidity_2m", 0), 1),
        "apparent_temp": round(c.get("apparent_temperature", 0), 1),
        "wind_speed":    round(c.get("wind_speed_10m", 0), 1),
        "wind_dir":      c.get("wind_direction_10m", 0),
        "precipitation": c.get("precipitation", 0),
        "uv_index":      c.get("uv_index", 0),
        "cloud_cover":   c.get("cloud_cover", 0),
        "weather_code":  code,
        "description":   desc,
        "emoji":         emoji,
        "time":          c.get("time", ""),
    }


def parse_hourly(data: dict) -> list[dict]:
    """Return next 24 hours of forecast data."""
    h = data.get("hourly", {})
    times = h.get("time", [])[:24]
    rows = []
    for i, t in enumerate(times):
        code = h.get("weather_code", [0] * 24)[i]
        desc, emoji = get_wmo_description(code)
        rows.append({
            "time":          t,
            "temperature":   round(h.get("temperature_2m", [0])[i], 1),
            "humidity":      round(h.get("relative_humidity_2m", [0])[i], 1),
            "apparent_temp": round(h.get("apparent_temperature", [0])[i], 1),
            "precip_prob":   h.get("precipitation_probability", [0])[i],
            "wind_speed":    round(h.get("wind_speed_10m", [0])[i], 1),
            "emoji":         emoji,
            "description":   desc,
        })
    return rows


def parse_daily(data: dict) -> list[dict]:
    """Return 7-day daily forecast."""
    d = data.get("daily", {})
    dates = d.get("time", [])
    rows = []
    for i, date in enumerate(dates):
        code = d.get("weather_code", [0] * 7)[i]
        desc, emoji = get_wmo_description(code)
        rows.append({
            "date":          date,
            "temp_max":      round(d.get("temperature_2m_max", [0])[i], 1),
            "temp_min":      round(d.get("temperature_2m_min", [0])[i], 1),
            "apparent_max":  round(d.get("apparent_temperature_max", [0])[i], 1),
            "precip_sum":    round(d.get("precipitation_sum", [0])[i], 1),
            "wind_max":      round(d.get("wind_speed_10m_max", [0])[i], 1),
            "uv_max":        d.get("uv_index_max", [0])[i],
            "sunrise":       d.get("sunrise", [""])[i],
            "sunset":        d.get("sunset", [""])[i],
            "emoji":         emoji,
            "description":   desc,
        })
    return rows

