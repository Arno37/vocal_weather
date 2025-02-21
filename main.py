from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import router  # Assurez-vous que ce fichier est bien importé

app = FastAPI()  # Création de l'application FastAPI

#  Ajout du montage des fichiers statiques après la création de `app`
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclusion des routes définies dans `router.py`
app.include_router(router)

# Lancer le serveur avec : uvicorn main:app --reload
