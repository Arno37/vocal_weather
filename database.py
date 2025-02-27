from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Remplace avec tes infos Azure
DATABASE_URL = "mssql+pyodbc://arnaud:GRETAP4!2025***@SERVEUR.database.windows.net/NOM_BASE?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Définition du modèle de données
class WeatherRequest(Base):
    __tablename__ = "weather_requests"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    request_time = Column(DateTime, default=datetime.utcnow)
    voice_command = Column(String)
    weather_response = Column(JSON)

# Création des tables
Base.metadata.create_all(bind=engine)
