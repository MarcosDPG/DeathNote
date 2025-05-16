from fastapi import HTTPException

from app.firebase.db import (
    obtener_criminal_death_note,
    actualizar_muerte_deathnote,
    EstadoCriminal
)

from app.events.eventos import publish_event
from app.models.models import DetallesMuerteRequest

async def escribir_detalles_muerte(detalles_muerte_request: DetallesMuerteRequest) -> dict:
    try:
        criminal = await obtener_criminal_death_note(detalles_muerte_request.criminal_id.strip())

        if not criminal:
            raise HTTPException(status_code=404, detail="Criminal no encontrado en la Death Note")

        criminal_data = criminal["data"]
        criminal_ref = criminal["ref"]

        # Verificar si el criminal ya ha sido ejecutado
        if criminal_data["proceso"] != EstadoCriminal.ASIGNADO.value:
            raise HTTPException(status_code=400, detail="El criminal ya ha sido ejecutado o no se le ha asignado causa de muerte")

        criminal_data["detalles_muerte"] = detalles_muerte_request.detalles_muerte
        criminal_data["proceso"] = EstadoCriminal.DETALLADO.value

        # Actualizar en la base de datos
        await actualizar_muerte_deathnote(criminal_ref, criminal_data)
        # Establcer detalles de muerte después para que el criminal se ejecute en 40 segundos
        await publish_event("DetallesMuerte", criminal_data)

        return {"mensaje": f"Se han asignado los detalles de muerte '{detalles_muerte_request.detalles_muerte}' al criminal {criminal_data['nombre_completo']}, morirá en 40 segundos."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al escribir en la Death Note: {e}")