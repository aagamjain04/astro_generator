import swisseph as swe
from geopy.geocoders import Nominatim
from datetime import datetime

# Initialize geolocator
geolocator = Nominatim(user_agent="astro_report_generator")

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

PLANET_MAP = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Venus": swe.VENUS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN
}

def get_coordinates(city: str, country: str):
    location = geolocator.geocode(f"{city}, {country}")
    if not location:
        raise ValueError("Could not find coordinates for the provided city and country.")
    return location.latitude, location.longitude

def calculate_chart(dob: str, tob: str, city: str, country: str):
    # Get Lat / Lon
    lat, lon = get_coordinates(city, country)

    # Parse Date and Time (Assuming UTC for simplicity in this baseline)
    # In production, you'd convert local time to UTC based on coordinates
    dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
    year, month, day, hour = dt.year, dt.month, dt.day, dt.hour + (dt.minute / 60.0)

    # Calculate Julian Day
    julday = swe.julday(year, month, day, hour)

    # Calculate Ascendant and Houses (Placidus system 'P')
    houses, ascmc = swe.houses(julday, lat, lon, b'P')
    ascendant_degree = ascmc[0]
    ascendant_sign = SIGNS[int(ascendant_degree / 30)]

    chart_data = {
        "ascendant": ascendant_sign,
        "planets": {}
    }

    # Calculate Planets
    for planet_name, planet_id in PLANET_MAP.items():
        # calc_ut returns a tuple: (longitude, latitude, distance, speed in long, speed in lat, speed in dist)
        planet_info, _ = swe.calc_ut(julday, planet_id)
        longitude = planet_info[0]

        sign_index = int(longitude / 30)
        sign_name = SIGNS[sign_index]

        # Simple house approximation: (Planet Sign index - Ascendant Sign index + 12) % 12 + 1
        asc_index = int(ascendant_degree / 30)
        house_num = ((sign_index - asc_index + 12) % 12) + 1

        chart_data["planets"][planet_name] = {
            "sign": sign_name,
            "house": house_num
        }

    return chart_data