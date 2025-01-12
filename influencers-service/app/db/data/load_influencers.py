import os
import sys

# Ajusta el path para asegurarte de que la carpeta `app` esté en el path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from app.db.models import Influencer
from app.db.session import SessionLocal
import json

def load_influencers():
    """
    Carga los datos de influencers desde un archivo JSON a la base de datos.
    """
    print("Cargando influencers...")
    db = SessionLocal()
    try:
        with open(os.path.join(os.path.dirname(__file__), "influencers.json"), "r", encoding="utf-8") as file:
            influencers = json.load(file)
            for influencer in influencers:
                db_influencer = Influencer(
                    name=influencer["name"],
                    handle=influencer["handle"],
                    followers_count=influencer["followers_count"],
                    description=influencer.get("description", ""),
                    category=influencer.get("category", "")
                )
                db.add(db_influencer)
            db.commit()
            print("¡Influencers cargados exitosamente!")
    except Exception as e:
        print(f"Error al cargar influencers: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    load_influencers()
