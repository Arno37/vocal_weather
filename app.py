# app.py
from flask import Flask, render_template, request, jsonify
from speech_to_text import recognize_from_microphone
from nlp import extract_city
from meteo import get_weather

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", nom_app="Vocal Weather")

@app.route("/get_weather", methods=["POST"])
def process_audio():
    """Capture l'audio, extrait la ville et renvoie la météo."""
    spoken_text = recognize_from_microphone()
    if not spoken_text:
        return jsonify({"error": "Aucune reconnaissance vocale détectée."})

    city = extract_city(spoken_text)
    if not city:
        return jsonify({"error": "Aucune ville détectée dans l'audio."})

    weather_info = get_weather(city)
    return jsonify({"city": city, "weather": weather_info})

if __name__ == "__main__":
    app.run(debug=True)