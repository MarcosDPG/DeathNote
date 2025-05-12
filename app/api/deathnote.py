import asyncio
from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.firebase.db import *

from app.sockets.connection_manager import notificar_muerte

router = APIRouter(prefix="/api/deathnote")

class DeathNoteRequest(BaseModel):
    nombres: str
    apellidos: str

# Esperar 40 segundos antes de asignar la muerte por defecto y notificar a los clientes conectados
async def asignar_muerte_defecto(criminal_id: str):
    # Simular un retraso de 40 segundos antes
    await asyncio.sleep(5)
    # Revisar los datos del criminal en la death note
    criminal_info = await obtener_criminal_death_note(criminal_id)
    # Verificar si el criminal existe y su estado es "pendiente"
    if not criminal_info or criminal_info["data"]["proceso"] != EstadoCriminal.PENDIENTE.value:
        return {"error": "El criminal no existe o ya ha sido ejecutado."}

    criminal_data = criminal_info["data"]
    criminal_ref = criminal_info["ref"]

    # Actualizar los datos localmente
    criminal_data["causa_muerte"] = "Ataque al corazón"
    criminal_data["proceso"] = EstadoCriminal.MUERTO.value
    criminal_data["fecha_ejecucion"] = datetime.now().isoformat()

    # Actualizar en la base de datos
    await actualizar_muerte_deathnote(criminal_ref, criminal_data)

    # Convertir las fechas a cadenas para evitar problemas de serialización
    criminal_data["fecha_registro"] = str(criminal_data["fecha_registro"])
    criminal_data["fecha_ejecucion"] = str(criminal_data["fecha_ejecucion"])

    # Actualizar el estado del criminal a muerto en la colección de criminales
    actualizar_estado_criminal(criminal_id)

    # Notificar a todos los clientes conectados
    await notificar_muerte(criminal_data)

    return {"mensaje": f"Criminal {criminal_id} ejecutado exitosamente"}


@router.post("/")
async def escribir_muerte(request: DeathNoteRequest, background_tasks: BackgroundTasks):
    try:
        resultado = escribir_nombre_deathnote(
            nombres=request.nombres,
            apellidos=request.apellidos
        )
        # Si no se especifica causa de muerte, asignar una por defecto
        background_tasks.add_task(asignar_muerte_defecto, resultado["criminal_id"])

        return {"id": resultado["criminal_id"], "mensaje": f"{resultado['nombre_completo']} será ejecutado en 40 segundos si no se especifica la causa."}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al escribir en la Death Note: {e}")

