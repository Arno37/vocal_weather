from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from services.weather import get_weather 
  # Import correct


router = APIRouter()

# Configurer Jinja2Templates avec le répertoire 'templates'
templates = Jinja2Templates(directory="templates")

# Route de la page d'accueil
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nom_app": "Météo App"})

@router.post("/weather", response_class=JSONResponse)
async def get_weather_route(request: Request, voice_command: str = Form(...)):
    print(f"Commande vocale reçue : {voice_command}")

    try:
        weather_data = get_weather(voice_command)  # 🔄 Vérifie que ça fonctionne
        print(f"Données météo obtenues : {weather_data}")
        return {"weather": weather_data}
    except Exception as e:
        print(f"Erreur interne : {str(e)}")  # Ajoute un log d'erreur
        return JSONResponse(content={"error": str(e)}, status_code=500)