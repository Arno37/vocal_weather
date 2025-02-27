import psycopg2

# Connexion à PostgreSQL sur Azure
HOST = "vw-arnaud.postgres.database.azure.com"
DATABASE = "postgres"  # Mets ici le bon nom de base
USER = "arnaud"
PASSWORD = "GRETAP4!2025***"

def get_db_connection():
    """Établit une connexion à PostgreSQL sur Azure."""
    try:
        print("🔄 Tentative de connexion à PostgreSQL...")  # Ajout d'un log
        conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=5432
        )
        print("✅ Connexion réussie à PostgreSQL Azure !")  # Log de succès
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion à PostgreSQL : {e}")
        return None

# Lancer la connexion pour tester
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        conn.close()
        print("🔌 Connexion fermée proprement.")
    else:
        print("❌ Impossible d'établir une connexion.")

def create_weather_table():
    if __name__ == "__main__":
    create_weather_table()

    """Crée la table Weather si elle n'existe pas."""
    conn = get_db_connection()
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
        
