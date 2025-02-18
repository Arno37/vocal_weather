import openmeteo_requests
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim

# Configuration du cache et de la gestion des erreurs
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Fonction pour récupérer les coordonnées d'une ville
def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city_name)
    
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Demander à l'utilisateur une ville
ville = input("Entrez une ville : ")
coords = get_coordinates(ville)

if coords:
    print(f"Coordonnées de {ville} : {coords[0]}, {coords[1]}")

    # Mise à jour des paramètres avec les coordonnées de la ville recherchée
    params = {
        "latitude": coords[0],
        "longitude": coords[1],
        "hourly": "temperature_2m"
    }

    # Appel à l'API Open-Meteo avec les coordonnées dynamiques
    responses = openmeteo.weather_api("https://api.open-meteo.com/v1/forecast", params=params)

    # Extraction des données météo
    response = responses[0]
    print(f"Météo de {ville} :")

else:
    print("⚠ Ville non trouvée.")
