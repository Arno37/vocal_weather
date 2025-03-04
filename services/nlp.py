import stanza
import re

# Télécharger le modèle français si nécessaire
stanza.download("fr")

# Initialiser le pipeline NLP avec Tokenization, POS et NER
nlp = stanza.Pipeline("fr", processors="tokenize,pos,ner")

def clean_text(text):
    """Nettoie le texte transcrit pour éviter les erreurs NLP"""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)  # Remplace les espaces multiples par un seul
    text = re.sub(r'[^\w\s]', '', text)  # Supprime la ponctuation (évite les erreurs avec aujourd'hui)
    text = re.sub(r'\b(euh|bah|heu|mmm|ben|ouais|voilà)\b', '', text)  # Supprime les mots parasites

    # Correction : Remplacement des expressions accentuées pour correspondre aux regex
    text = text.replace("aujourd'hui", "aujourdhui").replace("après-demain", "apresdemain")

    print(f"📌 Texte après nettoyage : {text}")  # 🔥 Debug
    return text


def extract_city_and_horizon(text):
    """Extrait le nom de la ville et l'horizon temporel du texte"""
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text)

    print(f"\n🔎 Texte analysé : {cleaned_text}")  # Debug

    city = None
    horizon = None

    # 🔹 Étape 1 : Extraction de la ville (ignorer "aujourd'hui", "demain", etc.)
    words = cleaned_text.split()
    for word in words:
        if word in KNOWN_CITIES:
            city = word
            break

    print(f"🏙 Ville détectée : {city}")  # Debug
    

    # 🔹 Étape 2 : Extraction de l'horizon temporel avec regex
    horizon_patterns = [
        r"\b(dans\s+\d+\s+(jours|semaines|mois|ans))\b",
        r"\b(la semaine prochaine|le mois prochain|l annee prochaine)\b",
        r"\b(demain|apresdemain|aujourdhui)\b"  # Correction : "aujourdhui" et "apresdemain" sans apostrophe
    ]

    for pattern in horizon_patterns:
        match = re.search(pattern, cleaned_text, re.IGNORECASE)
        if match:
            horizon = match.group(0)
            break

    print(f"📅 Horizon détecté : {horizon}")  # Debug

    return city, horizon
if __name__ == "__main__":
    # 🛠 Test du NLP
    test_sentences = [
        "Quel temps fait-il à Tours aujourd'hui ?",
        "Météo pour Paris la semaine prochaine",
        "Prévisions à Bordeaux demain",
        "Quel temps à Lille après-demain ?"
    ]

    print("\n🚀 TEST AUTOMATIQUE DE NLP :")
    for sentence in test_sentences:
        city, horizon = extract_city_and_horizon(sentence)
        print(f"🔍 Phrase : {sentence}")
        print(f"🏙 Ville détectée : {city}")
        print(f"📅 Horizon détecté : {horizon}\n")