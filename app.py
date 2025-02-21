from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

# Monter le répertoire 'static' pour servir les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurer Jinja2Templates avec le répertoire 'templates'
templates = Jinja2Templates(directory="templates")

# Route pour la page d'accueil
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nom_app": "Météo App'"})

# Route pour traiter le formulaire
@app.post("/weather", response_class=JSONResponse)
async def get_weather(request: Request, voice_command: str = Form(...)):
    print(f"Commande vocale reçue du front-end: {voice_command}")

    # Simulation de la réponse
    weather_data = {
        "city": voice_command,
        "condition": "Ensoleillé",
        "temperature": "25°C",
        "forecast": "Prévisions pour les prochains jours : ..."
    }

    print(f"Réponse météo simulée: {weather_data}")
    return weather_data
