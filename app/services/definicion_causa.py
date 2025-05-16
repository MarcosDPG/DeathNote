from fastapi import HTTPException

from app.firebase.db import (
    obtener_criminal_death_note,
    actualizar_muerte_deathnote,
    EstadoCriminal
)
from app.events.eventos import publish_event
from app.models.models import CausaMuerteRequest

async def escribir_causa_muerte(causa_muerte_request: CausaMuerteRequest) -> dict:
    try:
        criminal = await obtener_criminal_death_note(causa_muerte_request.criminal_id.strip())

        if not criminal:
            raise HTTPException(status_code=404, detail="Criminal no encontrado en la Death Note")

        criminal_data = criminal["data"]
        criminal_ref = criminal["ref"]

        # Verificar si el criminal ya ha sido ejecutado
        if criminal_data["proceso"] != EstadoCriminal.PENDIENTE.value:
            raise HTTPException(status_code=400, detail="El criminal ya ha sido ejecutado o no está en estado pendiente")

        criminal_data["causa_muerte"] = causa_muerte_request.causa_muerte
        criminal_data["proceso"] = EstadoCriminal.ASIGNADO.value
        # Pasarlo a string para evitar problemas de serialización
        criminal_data["fecha_registro"] = str(criminal_data["fecha_registro"])
        # Actualizar en la base de datos
        await actualizar_muerte_deathnote(criminal_ref, criminal_data)

        # Crear evento de causa de muerte
        await publish_event("CausaMuerte", criminal_data)

        return {"mensaje": f"Se ha asignado la causa de muerte '{causa_muerte_request.causa_muerte}' al criminal {criminal_data['nombre_completo']}, tienes 400 segundos para dar detalles."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al escribir en la Death Note: {e}")