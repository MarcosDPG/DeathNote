from fastapi import HTTPException

from app.firebase.db import escribir_nombre_deathnote

from app.models.models import DeathNoteRequest


from app.events.eventos import publish_event

async def escribir_muerte(request: DeathNoteRequest) -> dict:
    try:
        # Registrar el criminal en la base de datos
        resultado = escribir_nombre_deathnote(request.criminal_id.strip())
        resultado["fecha_registro"] = str(resultado["fecha_registro"])
        # Si no se especifica causa de muerte, asignar una por defecto
        await publish_event("MuertePorDefecto", resultado)

        return {"id": resultado["criminal_id"], "mensaje": f"{resultado['nombre_completo']} será ejecutado en 40 segundos si no se especifica la causa."}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    #except Exception as e:
    #    raise HTTPException(status_code=400, detail=f"Error al escribir en la Death Note: {e}")