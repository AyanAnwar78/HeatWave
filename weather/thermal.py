"""
Thermal stress calculations for HeatGuard.

Heat Index formula: Steadman (1979) / NWS regression
WBGT approximation available for future upgrade.
"""

# ── Risk category thresholds (°C heat-index) ─────────────────────────────────
RISK_LEVELS = [
    (27,  "Low",             "#22c55e", "🟢"),
    (32,  "Caution",         "#facc15", "🟡"),
    (41,  "Extreme Caution", "#f97316", "🟠"),
    (54,  "Danger",          "#ef4444", "🔴"),
    (None,"Extreme Danger",  "#7f1d1d", "🔴"),
]

SAFETY_TIPS = {
    "Low": [
        "Stay hydrated – drink water regularly.",
        "Wear light, breathable clothing.",
        "Normal outdoor activities are safe.",
    ],
    "Caution": [
        "Drink water every 15–20 minutes during exertion.",
        "Take breaks in shaded or cool areas.",
        "Avoid strenuous activities during peak sun hours (11 AM – 4 PM).",
        "Wear sunscreen SPF 30+.",
    ],
    "Extreme Caution": [
        "Limit outdoor exposure – risk of heat cramps and heat exhaustion.",
        "Carry water at all times; at least 500 ml per hour.",
        "Wear a wide-brimmed hat and UV-protective clothing.",
        "Check on elderly neighbours and young children.",
        "If sweating heavily, replenish electrolytes.",
    ],
    "Danger": [
        "⚠️ HIGH ALERT – heat stroke is possible.",
        "Stay indoors with air-conditioning or fans.",
        "Emergency: move to a cool place immediately if feeling dizzy or confused.",
        "Wet towels or cool showers help lower body temperature.",
        "Do not leave children or pets in parked vehicles.",
        "Call emergency services if someone collapses.",
    ],
    "Extreme Danger": [
        "🚨 EXTREME DANGER – heat stroke highly likely.",
        "Do NOT go outdoors unless absolutely necessary.",
        "Contact local emergency services for welfare checks.",
        "Open cooling centres in your area may be available.",
        "Continuous hydration is critical – do not wait until thirsty.",
    ],
}


def calculate_heat_index(temp_c: float, humidity: float) -> float:
    """
    Calculate the apparent temperature (heat index) in °C.

    Uses the NWS regression formula adapted for Celsius.
    Valid for temp >= 27°C and humidity >= 40%.
    For cooler/drier conditions returns temp_c directly.
    """
    T = temp_c
    RH = humidity

    # Simple estimate when conditions are mild
    if T < 27 or RH < 40:
        return round(T, 1)

    # Rothfusz regression (°F input converted internally)
    T_f = T * 9 / 5 + 32
    HI_f = (
        -42.379
        + 2.04901523 * T_f
        + 10.14333127 * RH
        - 0.22475541 * T_f * RH
        - 0.00683783 * T_f ** 2
        - 0.05481717 * RH ** 2
        + 0.00122874 * T_f ** 2 * RH
        + 0.00085282 * T_f * RH ** 2
        - 0.00000199 * T_f ** 2 * RH ** 2
    )

    # Adjustments
    if RH < 13 and 80 < T_f < 112:
        HI_f -= ((13 - RH) / 4) * ((17 - abs(T_f - 95)) / 17) ** 0.5
    elif RH > 85 and 80 < T_f < 87:
        HI_f += ((RH - 85) / 10) * ((87 - T_f) / 5)

    HI_c = (HI_f - 32) * 5 / 9
    return round(HI_c, 1)


def classify_risk(heat_index_c: float) -> dict:
    """Return risk category, colour, emoji, tips for a given heat index (°C)."""
    for threshold, level, colour, emoji in RISK_LEVELS:
        if threshold is None or heat_index_c < threshold:
            return {
                "level": level,
                "colour": colour,
                "emoji": emoji,
                "tips": SAFETY_TIPS[level],
            }

