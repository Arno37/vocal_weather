import openmeteo_requests
import requests
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim

# Configuration du cache et de la gestion des erreurs
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Fonction pour récupérer les coordonnées d'une ville
def get_coordinates(city_name):
    """Retourne les coordonnées GPS d'une ville."""
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city_name)
    
    return (location.latitude, location.longitude) if location else None

# Dictionnaire pour convertir les codes météo en texte lisible
WEATHER_CODES = {
    0: "Ciel clair",
    1: "Principalement clair",
    2: "Partiellement nuageux",
    3: "Nuageux",
    45: "Brouillard",
    48: "Brouillard givrant",
    51: "Bruine légère",
    53: "Bruine modérée",
    55: "Bruine dense",
    61: "Pluie faible",
    63: "Pluie modérée",
    65: "Pluie forte",
    80: "Averses légères",
    81: "Averses modérées",
    82: "Averses fortes",
    95: "Orages légers",
    96: "Orages avec grêle",
    99: "Orages violents"
}

# Fonction principale pour récupérer la météo
def get_weather(city: str):

    # URL Open-Meteo avec latitude/longitude fixes pour tester (Paris)
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude=48.8566&longitude=2.3522&daily=temperature_2m_max,weathercode&timezone=auto"
    )
    print(f"🌍 URL appelée : {url}")

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(f"📊 Réponse JSON : {data}")

            if "daily" in data:
                forecasts = [
                    {
                        "date": date,
                        "temperature_max": temp_max,
                        "condition": WEATHER_CODES.get(code, "Condition inconnue")  # Conversion des codes météo

                    }
                    for date, temp_max, code in zip(
                        data["daily"]["time"], 
                        data["daily"]["temperature_2m_max"], 
                        data["daily"]["weathercode"]
                    )
                ]
                return {"city": city, "forecasts": forecasts}
            else:
                print("❌ Aucune donnée météo trouvée dans la réponse.")
                return None
        else:
            print(f"❌ Erreur HTTP : {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        return None