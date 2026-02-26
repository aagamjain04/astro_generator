# A small sample of deterministic mappings
INTERPRETATION_DB = {
    "ascendant": {
        "Aries": "You approach the world with headfirst energy and a pioneering spirit. You are seen as bold and direct.",
        "Taurus": "You project a calm, stable, and reliable aura. People see you as grounded and practical.",
        # Add the rest...
    },
    "planets": {
        "Sun": {
            "signs": {
                "Taurus": "Your core identity is rooted in stability, nature, and creating tangible value.",
                "Gemini": "You are endlessly curious, adaptable, and communicative at your core."
            },
            "houses": {
                2: "Your focus shines on personal resources, wealth-building, and self-worth.",
                5: "Your vitality is tied to creativity, romance, and joyful self-expression."
            }
        },
        "Moon": {
            "signs": {
                "Leo": "Emotionally, you seek warmth, recognition, and dramatic self-expression.",
                "Cancer": "You are deeply intuitive, nurturing, and emotionally tied to home and family."
            },
            "houses": {
                1: "You wear your heart on your sleeve. Your emotions are highly visible.",
                5: "You find emotional security through creative pursuits and playful interactions."
            }
        }
        # Expand for Mars, Venus, etc.
    }
}

def build_report_content(chart_data: dict) -> dict:
    """Maps computed placements to the pre-written text."""
    report = {
        "ascendant_text": INTERPRETATION_DB["ascendant"].get(
            chart_data["ascendant"], "A strong ascendant placement guiding your path."
        ),
        "planet_texts": []
    }

    for planet, data in chart_data["planets"].items():
        sign = data["sign"]
        house = data["house"]

        sign_text = INTERPRETATION_DB["planets"].get(planet, {}).get("signs", {}).get(sign, f"The {planet} in {sign} brings unique energy.")
        house_text = INTERPRETATION_DB["planets"].get(planet, {}).get("houses", {}).get(house, f"The {planet} in House {house} highlights this area of life.")

        report["planet_texts"].append({
            "planet": planet,
            "sign": sign,
            "house": house,
            "interpretation": f"{sign_text} {house_text}"
        })

    return report