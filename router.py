from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from services.weather import get_weather, save_weather_data
from services.nlp import extract_city_and_horizon

  # Import correct


router = APIRouter()

# Configurer Jinja2Templates avec le répertoire 'templates'
templates = Jinja2Templates(directory="templates")

# Route de la page d'accueil
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"nom_app": "Météo App"})


@router.post("/weather", response_class=JSONResponse)
async def get_weather_route(request: Request, voice_command: str = Form(...)):
    print(f"Commande vocale reçue : {voice_command}")

    try:
        weather_data = get_weather(voice_command)
        
        # Vérifie si les données météo sont valides avant de les stocker
        if "forecasts" in weather_data and weather_data["forecasts"]:
            save_weather_data(weather_data["city"], weather_data["forecasts"])

        return {"weather": weather_data}
    except Exception as e:
        print(f"❌ Erreur interne : {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)