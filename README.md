# ☀️ Vocal Weather App

## Description
Ce projet consiste à développer une **application météo interactive avec commande vocale**. L'utilisateur peut demander la météo à voix haute, et l'application analyse la requête pour fournir les prévisions correspondantes.

### 🎯 Objectifs
- **Transformer la voix en texte** avec un service d'IA (Azure Speech-to-Text).
- **Analyser le texte** pour extraire les informations clés (lieu, date).
- **Interroger une API météo** externe pour obtenir les prévisions.
- **Stocker les résultats en Azure** pour optimiser les performances et analyser les tendances.
- **Exposer les prévisions via une interface web**.

---
## 🏗 Architecture

### 📌 Services Utilisés
- **Reconnaissance vocale :** Azure Speech-to-Text
- **Analyse du langage :** Azure LUIS (Language Understanding)
- **Données météo :** API externe avec Open-Météo
- **Stockage :** Azure SQL Database
- **Hébergement backend :** Azure App Services / Azure Functions
- **Frontend :** FastAPI

### 🔗 Flux de travail
1. L'utilisateur **parle** (ex: "Quel temps fera-t-il à Lyon demain ?").
2. Azure Speech-to-Text **convertit la voix en texte**.
3. Azure LUIS **analyse la phrase** et extrait le **lieu** et l'**horizon de prévision**.
4. L'application **vérifie si la donnée est déjà stockée** en Azure.
   - **Si oui**, elle renvoie directement la météo stockée.
   - **Sinon**, elle **appelle l'API météo** externe et **stocke la réponse**.
5. L'application **affiche la météo** à l'utilisateur.

---
## 🚀 Installation et Configuration

### 🖥 Prérequis
- Python 3.x
- Compte Azure
- Clé API du site [https://api.meteo-concept.com/](https://open-meteo.com/)

### 📦 Installation
1. **Cloner le projet**
   ```sh
   git clone https://github.com/votre-repo/voice-weather-app.git
   cd voice-weather-app
   ```
2. **Créer un environnement virtuel et l’activer**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Sur macOS/Linux
   venv\Scripts\activate    # Sur Windows
   ```
3. **Installer les dépendances**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configurer les variables d'environnement** (créer un fichier `.env`)
   ```env
   SPEECH_KEY=your_azure_speech_key
   SPEECH_REGION=your_azure_speech_region
   API_KEY=your_weather_api_key
   AZURE_STORAGE_CONNECTION=your_azure_storage_connection
   ```
5. **Lancer l'application**
   ```sh
   python app.py
   ```

---
## 📡 API Utilisées

### 🎙 Azure Speech-to-Text
- Convertit la voix en texte.
- Docs : [Azure Speech Services](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/)

### 🤖 Azure LUIS (Language Understanding)
- Analyse la phrase et extrait les entités (lieu, date).
- Docs : [Azure LUIS](https://learn.microsoft.com/en-us/azure/cognitive-services/luis/)

### 🌦 API Météo (ex: OpenWeather)
- Fournit les prévisions météo.
- Docs : [Meteo Concept API](https://api.meteo-concept.com/)

---
## 🛠 Fonctionnalités et Améliorations Futures
✅ Commande vocale pour demander la météo.  
✅ Analyse NLP pour comprendre la requête utilisateur.  
✅ Connexion à une API météo externe.  
✅ Interface web intuitive avec Flask.  
⬜ Prédiction de la météo avec IA.  
⬜ Géolocalisation automatique pour détecter l'emplacement de l'utilisateur.  
⬜ Intégration avec des assistants vocaux (Google Assistant, Alexa).  

---
## 📜 Licence
Ce projet est sous licence MIT.

---
## 💬 Contact
Pour toute question ou suggestion, contactez [votre email] ou ouvrez une issue sur GitHub.

---
🚀 **Développé avec passion pour une expérience météo plus intuitive et accessible !**

