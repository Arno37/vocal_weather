from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from router import router  # Assurez-vous que ce fichier est bien importé
from pydantic import BaseModel
import database 

app = FastAPI(title="Application Météo", description="API pour la reconnaissance vocale et la météo", version="1.0")

# 🎨 Montage des fichiers statiques (CSS, JS, images, favicon)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🛑 Correction de l'erreur 404 sur le favicon
@app.get("/favicon.ico")
async def favicon():
    return RedirectResponse(url="/static/favicon.ico")

# 🔓 Activation du CORS pour permettre l'accès depuis un frontend (⚠️ À restreindre en production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔹 Permet toutes les origines (à sécuriser en prod)
    allow_credentials=True,
    allow_methods=["*"],  # 🔹 Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # 🔹 Autorise tous les headers
)

# 📩 Inclusion des routes définies dans `router.py`
app.include_router(router)

# 📬 Modèle pour gérer le feedback utilisateur
class Feedback(BaseModel):
    message: str

# 📝 Endpoint pour recevoir les feedbacks des utilisateurs
@app.post("/feedback")
async def receive_feedback(feedback: Feedback):
    print(f"📩 Feedback reçu : {feedback.message}")
    return {"message": "Feedback reçu, merci !"}

# ✅ Ajout d'un endpoint GET pour récupérer la météo via l'URL du navigateur
@app.get("/weather")
async def get_weather(city: str, days: int = Query(7, ge=1, le=7)):
    """Permet de récupérer la météo via une requête GET."""
    response = database.get_weather(city, days)  # 🔹 Accès via `database.get_weather`
    
    if "error" in response:
        raise HTTPException(status_code=404, detail=response["error"])

    return response

