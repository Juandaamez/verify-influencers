from app.db.session import Base, engine

# Eliminar todas las tablas
Base.metadata.drop_all(bind=engine)
print("Tablas eliminadas.")
