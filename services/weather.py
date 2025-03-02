import openmeteo_requests
import requests
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim
import datetime  
from database import get_db_connection

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
    0: "Ciel clair", 1: "Principalement clair", 2: "Partiellement nuageux", 3: "Nuageux",
    45: "Brouillard", 48: "Brouillard givrant", 51: "Bruine légère", 53: "Bruine modérée",
    55: "Bruine dense", 61: "Pluie faible", 63: "Pluie modérée", 65: "Pluie forte",
    80: "Averses légères", 81: "Averses modérées", 82: "Averses fortes", 95: "Orages légers",
    96: "Orages avec grêle", 99: "Orages violents"
}

# Fonction principale pour récupérer la météo
def get_weather(city: str, days: int = 7):
    """Récupère la météo pour une ville et un nombre de jours donné."""
    coordinates = get_coordinates(city)
    if not coordinates:
        print(f"❌ Ville introuvable : {city}")
        return {"error": "Ville introuvable"}

    latitude, longitude = coordinates
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,weathercode&timezone=auto"

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
                        "condition": WEATHER_CODES.get(code, "Condition inconnue")
                    }
                    for date, temp_max, code in zip(
                        data["daily"]["time"], data["daily"]["temperature_2m_max"], data["daily"]["weathercode"]
                    )
                ]

                if days == 1:
                    today = datetime.datetime.today().strftime("%d-%m-%dY")
                    today_forecast = next((f for f in forecasts if f["date"] == today), None)
                    result = {"city": city, "coordinates": {"latitude": latitude, "longitude": longitude},
                              "forecasts": [today_forecast]} if today_forecast else {"city": city, "coordinates": {"latitude": latitude, "longitude": longitude},
                              "forecasts": []}
                    return result

                result = {"city": city, "coordinates": {"latitude": latitude, "longitude": longitude},
                          "forecasts": forecasts[:days]}
                return result
            else:
                print("❌ Aucune donnée météo trouvée dans la réponse.")
                return {"city": city, "coordinates": {"latitude": latitude, "longitude": longitude}, "forecasts": []}
        else:
            print(f"❌ Erreur HTTP : {response.status_code}")
            return {"city": city, "coordinates": {"latitude": latitude, "longitude": longitude}, "forecasts": []}
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        return {"city": city, "coordinates": {"latitude": latitude, "longitude": longitude}, "forecasts": []}


def save_weather_data(city, forecasts):
    """Stocke les prévisions météo en base de données PostgreSQL."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Correction : PostgreSQL ne supporte pas "IF NOT EXISTS" dans une requête INSERT
        # ✅ On crée la table une seule fois au début (évite de répéter cette requête)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Weather (
                id SERIAL PRIMARY KEY,
                city VARCHAR(100) NOT NULL,
                date DATE NOT NULL,
                temperature_max FLOAT NOT NULL,
                condition TEXT NOT NULL
            );
        """)

        # ✅ Insertion des prévisions météo
        for forecast in forecasts:
            cursor.execute(
                """
                INSERT INTO Weather (city, date, temperature_max, condition)
                VALUES (%s, %s, %s, %s)
                """,
                (city, forecast["date"], forecast["temperature_max"], forecast["condition"])
            )

        conn.commit()
        print(f"✅ Données météo enregistrées pour {city}")

    except Exception as e:
        print(f"❌ Erreur lors de l'insertion en base : {str(e)}")
    finally:
        cursor.close()
        conn.close()