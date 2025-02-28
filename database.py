import psycopg2

# Connexion à PostgreSQL sur Azure
HOST = "vw-arnaud.postgres.database.azure.com"
DATABASE = "postgres"  # Mets ici le bon nom de base
USER = "arnaud"
PASSWORD = "GRETAP4!2025***"

def get_db_connection(show_log=True):
    """Établit une connexion à PostgreSQL sur Azure et affiche un log si demandé."""
    try:
        if show_log:
            print("🔄 Tentative de connexion à PostgreSQL...")  # Log affiché une seule fois
        conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=5432
        )
        if show_log:
            print("✅ Connexion réussie à PostgreSQL Azure !")
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion à PostgreSQL : {e}")
        return None

def create_weather_table():
    """Crée la table Weather si elle n'existe pas."""
    conn = get_db_connection(show_log=False)  # ✅ Pas besoin d'afficher le log ici
    if not conn:
        print("❌ Impossible d'obtenir une connexion à la base de données.")
        return

    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Weather (
                id SERIAL PRIMARY KEY,
                city VARCHAR(100) NOT NULL,
                date DATE NOT NULL,
                temperature_max FLOAT NOT NULL,
                condition TEXT NOT NULL
            );
        """)
        conn.commit()
        print("✅ Table Weather créée ou déjà existante.")
    except Exception as e:
        print(f"❌ Erreur lors de la création de la table : {e}")
    finally:
        cursor.close()
        conn.close()

def check_weather_table():
    """Affiche le contenu de la table Weather."""
    conn = get_db_connection(show_log=False)  # ✅ Pas besoin d'afficher le log ici
    if not conn:
        print("❌ Impossible d'obtenir une connexion à la base de données.")
        return

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Weather;")
        rows = cursor.fetchall()
        if rows:
            print("📊 Contenu de la table Weather :")
            for row in rows:
                print(row)
        else:
            print("🔍 La table Weather est vide.")
    except Exception as e:
        print(f"❌ Erreur lors de la lecture des données : {e}")
    finally:
        cursor.close()
        conn.close()

        def get_weather(city: str, days: int = 7):
            print(f"🔍 Récupération de la météo pour {city} sur {days} jours")
    return {"city": city, "forecasts": [{"date": "2024-02-29", "temperature_max": 15, "condition": "Ensoleillé"}]}

def get_weather(city: str, days: int = 7):
    """Retourne une météo simulée."""
    return {
        "city": city,
        "forecasts": [
            {"date": "2024-02-29", "temperature_max": 12, "condition": "Nuageux"}
        ]
    }



# 🔹 Exécuter le script uniquement si lancé directement
if __name__ == "__main__":
    conn = get_db_connection()  # ✅ Affiche la connexion réussie une seule fois
    if conn:
        conn.close()
    create_weather_table()
    check_weather_table()
