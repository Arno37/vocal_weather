from flask import Flask, render_template, request, jsonify
from speech_to_text import recognize_from_microphone
from nlp import extract_city
from meteo import get_weather

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Permet d'actualiser les templates automatiquement

@app.route("/")
def index():
    return render_template("index.html", nom_app="Météo App'")

@app.route("/weather", methods=["POST"])
def process_audio():
    spoken_text = request.form.get("voice_command", "")

    if not spoken_text:
        return jsonify({"error": "Aucune reconnaissance vocale détectée."})

    city = extract_city(spoken_text)
    if not city:
        return jsonify({"error": "Aucune ville détectée dans l'audio."})

    weather_info = get_weather(city)
    return jsonify({
        "city": city,
        "condition": weather_info.get("condition", "Inconnu"),
        "temperature": weather_info.get("temperature", "N/A"),
        "forecast": weather_info.get("forecast", "Non disponible")
    })

if __name__ == "__main__":
    app.run(debug=True)
