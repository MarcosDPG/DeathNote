from enum import Enum
from datetime import datetime

from google.cloud.firestore import FieldFilter

from .client import db

class EstadoCriminal(Enum):
    PENDIENTE = "pendiente" # Sin causa de muerte
    ASIGNADO = "asignado" # Cuando una muerte tien una causa
    DETALLADO = "detallado" # Cuando se especifica una causa de muerte
    MUERTO = "muerto"

def registrar_criminal(data: dict):
    """
    Guarda un criminal en la colección 'criminales'.
    """
    doc_ref = db.collection("criminales").document()
    doc_ref.set(data)
    return doc_ref.id

def actualizar_criminal(criminal_id: str, updates: dict):
    try:
        criminal_ref = db.collection("criminales").document(criminal_id)
        doc = criminal_ref.get()
        
        if not doc.exists:
            raise ValueError("El criminal no existe")
        
        updates_validos = {k: v for k, v in updates.items() if v is not None}
        
        if not updates_validos:
            raise ValueError("No se proporcionaron campos válidos para actualizar")
        
        # Actualización
        criminal_ref.update(updates_validos)
        
        # Devuelve un diccionario simple
        return {
            "id": criminal_id,
            **updates_validos,
            "estado": doc.get("estado")  # Mantenemos el estado existente
        }
        
    except Exception as e:
        raise ValueError(f"Error al actualizar criminal: {str(e)}")
def log_event(event_type: str, data: dict):
    db.collection("events").document().set({
        "type": event_type,
        "criminal_id": data.get("criminal_id"),
        "timestamp": datetime.now()
    })

def obtener_criminales():
    """
    Devuelve todos los criminales registrados.
    """
    docs = db.collection("criminales").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

def obtener_criminales_nombre(nombre: str):
    """
    Devuelve criminales que coincidan con el nombre y apellido.
    """
    query = db.collection("criminales")\
              .where(filter=FieldFilter("nombre", "==", nombre))\
              .stream()

    # Convertir los resultados a una lista de diccionarios
    resultados = []
    for doc in query:
        resultados.append({**doc.to_dict(), "id": doc.id})

    # Si no hay resultados, devolver None
    if not resultados:
        return None

    # Si hay múltiples resultados, devolver la lista
    return resultados

# Obtiene de la colección "deathnote" un criminal específico por su ID
async def obtener_criminal_death_note(criminal_id: str):
    """
    Devuelve un criminal específico por su ID junto con su referencia de documento.
    """
    query = db.collection("deathnote").where(filter=FieldFilter("criminal_id", "==", criminal_id)).limit(1).get()
    if not query:
        return None

    doc = query[0]
    return {"data": doc.to_dict(), "ref": doc.reference}

# Cambia el estado del criminal a "muerto"
def actualizar_estado_criminal(criminal_id: str):
    doc_ref = db.collection("criminales").document(criminal_id)
    doc_ref.update({"estado": "muerto"})

def escribir_nombre_deathnote(criminal_id: str):
    # 1. Buscar al criminal
    criminales_ref = db.collection("criminales")
    query = criminales_ref.document(criminal_id).get()

    if not query.exists:
        raise ValueError("El criminal no existe en la base de datos")

    criminal_data = query.to_dict()

    # 2. Verificar regla de la imagen
    if criminal_data.get("foto_base64", "no_foto") == "no_foto":
        raise ValueError("El criminal no tiene una foto registrada, no se puede ejecutar")

    # 3. Verficar que el criminal no esté sentenciado
    sentencia_query = db.collection("deathnote").where(filter=FieldFilter("criminal_id", "==", criminal_id)).limit(1).get()

    # Si ya existe un registro para este criminal
    if sentencia_query:
        raise ValueError("Este criminal ya ha sido sentenciado")

    # 4. Registrar en la Death Note
    deathnote_ref = db.collection("deathnote").document()
    muerte_data = {
        "criminal_id": criminal_id,
        "nombre_completo": criminal_data['nombre_completo'],
        "causa_muerte": "",
        "detalles_muerte": "",
        "fecha_registro": datetime.now(),
        "fecha_ejecucion": None,
        "proceso": EstadoCriminal.PENDIENTE.value
    }

    deathnote_ref.set(muerte_data)
    return muerte_data

# Actualiza la causa de muerte y el estado del criminal en la Death Note
async def actualizar_muerte_deathnote(criminal_ref, datos: dict):
    criminal_ref.update(datos)

async def obtener_hojas_deathnote():
    """
    Devuelve todos los registros de la deathnote.
    """
    docs = db.collection("deathnote").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]


"""
def listar_registros_deathnote():
    registros = db.collection("deathnote")\
                 .order_by("fecha_registro", direction=firestore.Query.DESCENDING)\
                 .stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in registros]

"""
