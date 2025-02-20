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
    if not text.endswith(('.', '!', '?')):  # Ajoute un point si nécessaire
        text += '.'
    return text

def extract_city(text):
    """Extrait le nom de la ville du texte"""
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text)

    for ent in doc.ents:
        if ent.type == "LOC":  # Vérifie si l'entité est une localisation
            return ent.text
    return None  # Retourne None si aucune ville n'est détectée

# 🔍 Exemple de test (simulation du Speech-to-Text)
transcribed_text = "euh météo Paris demain"
city = extract_city(transcribed_text)

if city:
    print(f"🏙 Ville détectée : {city}")
else:
    print("⚠ Aucune ville détectée.")