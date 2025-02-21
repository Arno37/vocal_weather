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
import requests

def get_weather(city: str):
    print(f"🔎 Fonction `get_weather()` appelée avec : {city}")

    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true"
        print(f"🌍 Requête envoyée à OpenMeteo : {url}")

        response = requests.get(url)
        print(f"📡 Réponse brute de l'API : {response.status_code}, {response.text}")

        if response.status_code == 200:
            data = response.json()
            return data.get("current_weather", "❌ Aucune donnée météo reçue.")
        else:
            return f"❌ Erreur OpenMeteo : {response.status_code}"

    except Exception as e:
        print(f"❌ Exception attrapée : {str(e)}")
        return f"❌ Erreur : {str(e)}"
