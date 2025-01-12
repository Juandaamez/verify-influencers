import os
import sys

# Ajusta el path para asegurarte de que la carpeta `app` esté en el path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from app.db.session import Base, engine
from app.db.models import Influencer, Claim, User  # Asegúrate de importar explícitamente los modelos

def create_tables():
    """
    Crea las tablas en la base de datos basadas en los modelos definidos.
    """
    print("Creando tablas en la base de datos...")
    # Crea todas las tablas basadas en los modelos definidos
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas exitosamente!")

if __name__ == "__main__":
    create_tables()
