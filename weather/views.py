import json
from django.shortcuts import render
from django.http import JsonResponse

from .forms import CitySearchForm
from .services import geocode_city, fetch_weather, parse_current, parse_hourly, parse_daily
from .thermal import calculate_heat_index, classify_risk
from .models import WeatherSearch

DEFAULT_CITY = "Phagwara"


def _build_context(city_name: str) -> dict | None:
    """Fetch, parse, and enrich weather data for a city."""
    geo = geocode_city(city_name)
    if not geo:
        return None

    raw = fetch_weather(geo["latitude"], geo["longitude"], geo.get("timezone", "auto"))
    if not raw:
        return None

    current  = parse_current(raw)
    hourly   = parse_hourly(raw)
    daily    = parse_daily(raw)

    hi   = calculate_heat_index(current["temperature"], current["humidity"])
    risk = classify_risk(hi)

    # Flag hot days (apparent max ≥ 35°C)
    for day in daily:
        day_hi   = calculate_heat_index(day["temp_max"], 60)   # 60% approx
        day_risk = classify_risk(day_hi)
        day["heat_index"]  = day_hi
        day["risk"]        = day_risk
        day["is_hot"]      = day["apparent_max"] >= 35

    # Chart data (hourly temps + heat index for next 24 h)
    chart_labels    = [h["time"][-5:] for h in hourly]          # HH:MM
    chart_temps     = [h["temperature"] for h in hourly]
    chart_feels     = [h["apparent_temp"] for h in hourly]
    chart_humidity  = [h["humidity"] for h in hourly]
    chart_hi        = [calculate_heat_index(h["temperature"], h["humidity"]) for h in hourly]

    return {
        "city":        geo["name"],
        "country":     geo["country"],
        "latitude":    geo["latitude"],
        "longitude":   geo["longitude"],
        "timezone":    geo.get("timezone", "UTC"),
        "current":     current,
        "hourly":      hourly,
        "daily":       daily,
        "heat_index":  hi,
        "risk":        risk,
        # JSON-safe chart data
        "chart_labels":   json.dumps(chart_labels),
        "chart_temps":    json.dumps(chart_temps),
        "chart_feels":    json.dumps(chart_feels),
        "chart_humidity": json.dumps(chart_humidity),
        "chart_hi":       json.dumps(chart_hi),
    }


def _save_search(ctx: dict):
    """Persist search to DB (silently ignore errors)."""
    try:
        WeatherSearch.objects.create(
            city=ctx["city"],
            country=ctx["country"],
            latitude=ctx["latitude"],
            longitude=ctx["longitude"],
            temperature=ctx["current"]["temperature"],
            humidity=ctx["current"]["humidity"],
            wind_speed=ctx["current"]["wind_speed"],
            heat_index=ctx["heat_index"],
            risk_level=ctx["risk"]["level"],
        )
    except Exception:
        pass


# ── Views ─────────────────────────────────────────────────────────────────────

def dashboard(request):
    form = CitySearchForm(request.GET or None)
    city = DEFAULT_CITY
    error = None

    if form.is_valid():
        city = form.cleaned_data["city"].strip()

    ctx = _build_context(city)
    if ctx is None:
        error = f'Could not find weather data for "{city}". Please try another city.'
        ctx   = _build_context(DEFAULT_CITY) or {}

    if ctx:
        _save_search(ctx)

    ctx.update({"form": form, "error": error, "searched_city": city})
    return render(request, "weather/dashboard.html", ctx)


def forecast(request):
    form = CitySearchForm(request.GET or None)
    city = request.GET.get("city", DEFAULT_CITY).strip() or DEFAULT_CITY

    ctx = _build_context(city)
    if ctx is None:
        ctx = _build_context(DEFAULT_CITY) or {}

    ctx.update({"form": form})
    return render(request, "weather/forecast.html", ctx)


def heatmap(request):
    """
    Heat risk map: compare multiple cities.
    Accepts ?cities=CityA,CityB,CityC or falls back to defaults.
    """
    cities_param = request.GET.get("cities", "")
    city_list = [c.strip() for c in cities_param.split(",") if c.strip()]
    if not city_list:
        city_list = ["Phagwara", "Ludhiana", "Amritsar", "Jalandhar",
                     "Chandigarh", "Delhi", "Mumbai", "Chennai"]

    markers = []
    for city_name in city_list:
        geo = geocode_city(city_name)
        if not geo:
            continue
        raw = fetch_weather(geo["latitude"], geo["longitude"])
        if not raw:
            continue
        cur  = parse_current(raw)
        hi   = calculate_heat_index(cur["temperature"], cur["humidity"])
        risk = classify_risk(hi)
        markers.append({
            "name":        geo["name"],
            "country":     geo["country"],
            "lat":         geo["latitude"],
            "lon":         geo["longitude"],
            "temperature": cur["temperature"],
            "humidity":    cur["humidity"],
            "heat_index":  hi,
            "risk_level":  risk["level"],
            "colour":      risk["colour"],
            "emoji":       risk["emoji"],
        })

    return render(request, "weather/heatmap.html", {
        "markers":        markers,
        "markers_json":   json.dumps(markers),
        "cities_input":   ", ".join(city_list),
        "form":           CitySearchForm(),
    })


def about(request):
    return render(request, "weather/about.html", {"form": CitySearchForm()})


def api_weather(request):
    """JSON endpoint for quick city lookups (used by JS search suggestion)."""
    city = request.GET.get("city", "").strip()
    if not city:
        return JsonResponse({"error": "No city provided"}, status=400)
    ctx = _build_context(city)
    if ctx is None:
        return JsonResponse({"error": "City not found"}, status=404)
    return JsonResponse({
        "city":        ctx["city"],
        "country":     ctx["country"],
        "temperature": ctx["current"]["temperature"],
        "humidity":    ctx["current"]["humidity"],
        "wind_speed":  ctx["current"]["wind_speed"],
        "heat_index":  ctx["heat_index"],
        "risk_level":  ctx["risk"]["level"],
        "colour":      ctx["risk"]["colour"],
    })
