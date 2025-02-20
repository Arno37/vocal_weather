import openmeteo_requests
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim

# Configuration du cache et de la gestion des erreurs
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_coordinates(city_name):
    """Retourne les coordonnées GPS d'une ville."""
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city_name)
    
    return (location.latitude, location.longitude) if location else None

def get_weather(city):
    """Retourne la météo d'une ville en fonction de ses coordonnées."""
    coords = get_coordinates(city)
    if not coords:
        return f"⚠ Ville '{city}' non trouvée."

    params = {"latitude": coords[0], "longitude": coords[1], "hourly": "temperature_2m"}
    
    try:
        responses = openmeteo.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
        temperature = responses[0]["hourly"]["temperature_2m"][0]
        return f"🌤 La température actuelle à {city} est de {temperature}°C."
    except Exception as e:
        return f"❌ Erreur lors de la récupération des données météo : {str(e)}"

# 🔍 TEST UNIQUEMENT SI LE SCRIPT EST EXÉCUTÉ DIRECTEMENT
if __name__ == "__main__":
    ville = input("Entrez une ville : ")
    print(get_weather(ville))