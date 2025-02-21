import stanza
import re

# Télécharger le modèle français si nécessaire
stanza.download("fr")

# Initialiser le pipeline NLP avec Tokenization, POS et NER
nlp = stanza.Pipeline("fr", processors="tokenize,pos,ner")

def clean_text(text):
    """Nettoie le texte transcrit pour éviter les erreurs NLP"""
    text = text.lower().strip()  # Mise en minuscules et suppression des espaces inutiles
    text = re.sub(r'\s+', ' ', text)  # Remplace plusieurs espaces par un seul
    text = re.sub(r'[^a-zA-ZÀ-ÿ0-9\s]', '', text)  # Supprime caractères spéciaux sauf espaces
    text = re.sub(r'\b(euh|bah|heu|mmm|ben|ouais|voilà)\b', '', text)  # Supprime les mots parasites
    return text

def extract_city_and_horizon(text):
    """Extrait le nom de la ville et l'horizon temporel du texte"""
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text)

    city = None
    horizon = None

    # 🔹 Extraction des lieux (villes)
    for ent in doc.ents:
        if ent.type == "LOC":  # Vérifie si l'entité est une localisation
            city = ent.text
            break  # On prend la première ville détectée

    # 🔹 Extraction des horizons temporels avec regex
    horizon_patterns = [
        r"\b(dans\s+\d+\s+(jours|semaines|mois|ans))\b",
        r"\b(la semaine prochaine|le mois prochain|l'année prochaine)\b",
        r"\b(demain|après-demain|aujourd'hui)\b"
    ]

    for pattern in horizon_patterns:
        match = re.search(pattern, cleaned_text, re.IGNORECASE)
        if match:
            horizon = match.group(0)  # Prend la première correspondance trouvée
            break

    return city, horizon

# 🔍 Exemple de test (simulation du Speech-to-Text)
transcribed_text = "euh météo Paris dans 3 jours"
city, horizon = extract_city_and_horizon(transcribed_text)

if city:
    print(f"🏙 Ville détectée : {city}")
else:
    print("⚠ Aucune ville détectée.")

if horizon:
    print(f"📅 Horizon détecté : {horizon}")
else:
    print("⚠ Aucun horizon temporel détecté.")
