import stanza
import re

# Télécharger le modèle français si nécessaire
stanza.download("fr")

# Initialiser le pipeline NLP avec Tokenization, POS et NER
nlp = stanza.Pipeline("fr", processors="tokenize,pos,ner")

def clean_transcribed_text(text):
    """Nettoie le texte transcrit pour éviter les erreurs NLP"""
    text = text.lower().strip()  # Mise en minuscules et suppression des espaces inutiles
    text = re.sub(r'\s+', ' ', text)  # Remplace plusieurs espaces par un seul
    text = re.sub(r'[^a-zA-ZÀ-ÿ0-9\s]', '', text)  # Supprime caractères spéciaux sauf espaces
    text = re.sub(r'\b(euh|bah|heu|mmm|ben|ouais|voilà)\b', '', text)  # Supprime les mots parasites
    return text.strip()

def check_sentence_completeness(text):
    """Ajoute un point si la phrase semble incomplète"""
    if not text.endswith(('.', '!', '?')):
        return text + '.'
    return text

def analyze_text(text):
    """Nettoie, vérifie et analyse un texte transcrit"""
    cleaned_text = clean_transcribed_text(text)
    checked_text = check_sentence_completeness(cleaned_text)

    print(f"\n🎤 Texte nettoyé : {checked_text}")

    # Exécuter le NLP
    doc = nlp(checked_text)

    print("Tokenization et Part-of-Speech Tagging :")
    for sentence in doc.sentences:
        for word in sentence.words:
            print(f"{word.text} -> {word.upos}")

    print("Reconnaissance d'Entités Nommées (NER) :")
    if not doc.ents:
        print("Aucune entité nommée détectée.")
    else:
        for sentence in doc.sentences:
            for ent in sentence.ents:
                print(f"Entité : {ent.text}, Type : {ent.type}")

# 🔍 Exemple de phrase transcrite (simulation du Speech-to-Text)
transcribed_text = "euh météo Paris demain"
analyze_text(transcribed_text)
