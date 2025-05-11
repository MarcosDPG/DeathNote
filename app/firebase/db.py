from .client import db
from datetime import datetime, timedelta
from google.cloud import firestore

def registrar_criminal(data: dict):
    """
    Guarda un criminal en la colección 'criminales'.
    """
    doc_ref = db.collection("criminales").document()
    doc_ref.set(data)
    return doc_ref.id

def obtener_criminales():
    """
    Devuelve todos los criminales registrados.
    """
    docs = db.collection("criminales").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

def escribir_en_deathnote(nombres: str, apellidos: str, causa: str = None, detalles: str = None):
    # 1. Buscar al criminal
    criminales_ref = db.collection("criminales")
    query = criminales_ref.where("nombres", "==", nombres)\
                         .where("apellidos", "==", apellidos)\
                         .limit(1).get()
    
    if not query:
        raise ValueError("El criminal no existe en la base de datos")
    
    criminal_doc = query[0]
    criminal_data = criminal_doc.to_dict()
    
    # 2. Verificar regla de la imagen
    puede_morir = criminal_data.get("foto_base64", "no_foto") != "no_foto"
    
    # 3. Registrar en la Death Note
    deathnote_ref = db.collection("deathnote").document()
    muerte_data = {
        "criminal_id": criminal_doc.id,
        "nombre_completo": f"{nombres} {apellidos}",
        "causa_muerte": causa or "ataque al corazón",
        "detalles_muerte": detalles or "",
        "fecha_registro": datetime.utcnow(),
        "ejecutado": puede_morir,
        "error": None if puede_morir else "El criminal no tiene imagen registrada"
    }
    
    # 4. Actualizar estado del criminal si puede morir
    if puede_morir:
        criminal_doc.reference.update({"estado": "muerto"})
    
    deathnote_ref.set(muerte_data)
    return muerte_data


"""
def listar_registros_deathnote():
    registros = db.collection("deathnote")\
                 .order_by("fecha_registro", direction=firestore.Query.DESCENDING)\
                 .stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in registros]

"""
