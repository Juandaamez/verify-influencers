import os
import sys
import json
from datetime import datetime

# Asegurarse de que el directorio raíz del proyecto esté en PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from app.db.session import SessionLocal  # Importación corregida
from app.db.models import Claim

# Inicializar la sesión de base de datos
db = SessionLocal()

# Eliminar todos los registros existentes de claims para evitar duplicados
db.query(Claim).delete()
db.commit()
print("Todos los registros de claims han sido eliminados.")

# Ruta del archivo JSON de claims
json_file_path = os.path.join(os.path.dirname(__file__), "claims.json")

# Leer el archivo JSON
with open(json_file_path, "r") as file:
    claims = json.load(file)

# Insertar los nuevos claims en la base de datos
for data in claims:
    claim = Claim(
        claim_text=data["claim_text"],
        confidence_score=data["confidence_score"],
        influencer_id=data["influencer_id"],
        date=datetime.strptime(data["date"], "%Y-%m-%d") if "date" in data else datetime.utcnow(),
    )
    db.add(claim)

# Confirmar los cambios
db.commit()
print("Claims cargados exitosamente en la base de datos.")

# Cerrar la sesión
db.close()
