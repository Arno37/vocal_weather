import stanza
import re

# Télécharger le modèle français si nécessaire
stanza.download("fr")

# Initialiser le pipeline NLP avec Tokenization, POS et NER
nlp = stanza.Pipeline("fr", processors="tokenize,pos,ner")

def clean_text(text):
    """Nettoie le texte transcrit pour éviter les erreurs NLP"""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-ZÀ-ÿ0-9\s]', '', text)
    text = re.sub(r'\b(euh|bah|heu|mmm|ben|ouais|voilà)\b', '', text)

    print(f"📌 Texte après nettoyage : {text}")  # 🔥 Debug
    return text

KNOWN_CITIES = {"paris", "lyon", "marseille", "toulouse", "bordeaux", "lille",
                "nantes", "strasbourg", "rennes", "montpellier", "nice","bruxelles", "genève", "londres", "berlin", "new york"}

def extract_city_and_horizon(text):
    """Extrait le nom de la ville et l'horizon temporel du texte"""
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text)

    print(f"\n🔎 Texte analysé : {cleaned_text}")  # Debug

    city = None
    horizon = None

    # 🔹 Extraction des lieux avec Stanza (LOC ou GPE)
    for ent in doc.entities:
        print(f"👉 Entité détectée : {ent.text} | Type : {ent.type}")  # Debug
        if ent.type in ["LOC", "GPE"]:  
            city = ent.text.lower()
            break  

    # 🔹 Si Stanza ne détecte pas de ville, vérifie dans la liste manuelle
    if city is None:
        words = cleaned_text.split()
        for word in words:
            if word in KNOWN_CITIES:
                city = word
                break

    print(f"🏙 Ville détectée : {city}")  # Debug

    # 🔹 Extraction des horizons temporels avec regex
    horizon_patterns = [
        r"\b(dans\s+\d+\s+(jours|semaines|mois|ans))\b",
        r"\b(la semaine prochaine|le mois prochain|l'année prochaine)\b",
        r"\b(demain|après-demain|aujourd'hui)\b"
    ]

    for pattern in horizon_patterns:
        match = re.search(pattern, cleaned_text, re.IGNORECASE)
        if match:
            horizon = match.group(0)  
            break

    print(f"📅 Horizon détecté : {horizon}")  # Debug

    return city, horizon
