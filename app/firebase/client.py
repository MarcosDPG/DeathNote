import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path


# Ruta relativa al archivo client.py
ruta_credenciales = os.path.join(Path(__file__).parent, "deathnote.json")

# Evita reinicializar si ya está inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(ruta_credenciales)
    firebase_admin.initialize_app(cred)

# Cliente de firestore
db = firestore.client()


