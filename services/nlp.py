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

def extract_city_and_horizon(voice_command):
    print(f"🔍 Commande reçue : {voice_command}")

    # Vérification rapide des villes reconnues
    if "paris" in voice_command.lower():
        return "Paris", 7
    if "lyon" in voice_command.lower():
        return "Lyon", 7
    if "marseille" in voice_command.lower():
        return "Marseille", 7
    print("❌ Aucune ville détectée")
    test_command = (voice_command)
    city, horizon = extract_city_and_horizon(test_command)
    print(f"🏙 Ville détectée : {city}, 📅 Horizon : {horizon}")
    return city, 7
