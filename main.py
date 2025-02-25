from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import router  # Assurez-vous que ce fichier est bien importé


app = FastAPI()  # Création de l'application FastAPI

# Instrumentation de l'API avec Prometheus (après la définition de `app`)
Instrumentator().instrument(app).expose(app)

# Ajout du montage des fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclusion des routes définies dans `router.py`
app.include_router(router)
