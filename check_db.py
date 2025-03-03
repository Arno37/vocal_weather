import psycopg2

# 🔹 Connexion à PostgreSQL (remplace avec tes infos)
HOST = "vw-arnaud.postgres.database.azure.com"
DATABASE = "postgres"
USER = "arnaud"
PASSWORD = "GRETAP4!2025***"

def check_weather_data():
    """Affiche les entrées stockées dans la table Weather."""
    try:
        conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=5432
        )
        cursor = conn.cursor()

        # Exécuter la requête pour afficher toutes les entrées
        cursor.execute("SELECT * FROM Weather;")
        rows = cursor.fetchall()

        if rows:
            print("📊 Données météo enregistrées :")
            for row in rows:
                print(row)
        else:
            print("🔍 Aucune donnée trouvée.")

    except Exception as e:
        print(f"❌ Erreur lors de la lecture des données : {e}")
    finally:
        cursor.close()
        conn.close()

# 🔹 Lancer la vérification
if __name__ == "__main__":
    check_weather_data()