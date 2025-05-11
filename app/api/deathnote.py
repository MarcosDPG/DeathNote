from fastapi import APIRouter, HTTPException
from app.firebase.db import escribir_en_deathnote
from pydantic import BaseModel

router = APIRouter(prefix="/api/deathnote")

class DeathNoteRequest(BaseModel):
    nombres: str
    apellidos: str
    causa_muerte: str = "ataque al corazón"
    detalles_muerte: str = ""

@router.post("/escribir")
async def escribir_muerte(request: DeathNoteRequest):
    try:
        resultado = escribir_en_deathnote(
            nombres=request.nombres,
            apellidos=request.apellidos,
            causa=request.causa_muerte,
            detalles=request.detalles_muerte
        )
        if not resultado["ejecutado"]:
            return {"advertencia": resultado["error"], "pagina_id": resultado["criminal_id"]}
        return {"mensaje": "Muelto", "pagina_id": resultado["criminal_id"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))