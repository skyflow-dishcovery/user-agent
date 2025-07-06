from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_location_from_coords(latitude: float, longitude: float) -> str:
    try:
        geolocator = Nominatim(user_agent="skyflow_app")
        location = geolocator.reverse((latitude, longitude), timeout=10)
        if location and location.address:
            return location.address
        return "Unknown location"
    except GeocoderTimedOut:
        return "Location request timed out"
    except Exception as e:
        return f"Location error: {str(e)}"
