import re
from datetime import datetime

KNOWN_CITIES = {"paris", "lyon", "marseille", "toulouse", "bordeaux", "lille",
                "nantes", "strasbourg", "rennes", "montpellier", "nice", "tours",
                "bruxelles", "genève", "londres", "berlin", "new york"}

def extract_city_and_horizon(command):
    """
    Extrait la ville et l'horizon temporel ("aujourd'hui", "7 jours", "15 jours") d'une commande vocale.
    """
    city = ""
    horizon = None

    # 🔍 Détection de la période demandée
    if "aujourd'hui" in command:
        horizon = "aujourd'hui"
    elif "15 jours" in command:
        horizon = "15 jours"
    elif "7 jours" in command:
        horizon = "7 jours"

    # 🔍 Extraction de la ville après "à" ou "de"
    match = re.search(r"\b(?:à|de)\s+(\w+)", command)
    if match:
        city = match.group(1).lower().strip()
    else:
        # Vérification si la ville est directement mentionnée dans la commande
        for known_city in KNOWN_CITIES:
            if known_city in command.lower():
                city = known_city
                break

    # Vérification si la ville est connue
    if city not in KNOWN_CITIES:
        city = ""

    print(f"🔍 Commande : {command}")
    print(f"🏙 Ville détectée : {city}")
    print(f"🕒 Horizon détecté : {horizon}")

    return city, horizon

def format_date(date_str):
    """
    Formate une date au format 'YYYY-MM-DD' en une date lisible.
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%d %B %Y')
