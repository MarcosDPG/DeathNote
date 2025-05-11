from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.firebase.db import registrar_criminal, obtener_criminales
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/criminales")

class Criminal(BaseModel):
    nombres: str
    apellidos: str
    foto_base64: Optional[str] = Field(default="no_foto")  # Campo opcional con valor por defecto
    estado: str = "vivo"
    registrado_en: str = datetime.utcnow().isoformat()  # Genera automáticamente la fecha

@router.get("/")
async def listar_criminales():
    try:
        criminales = obtener_criminales()
        return {"criminales": criminales}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/registrar")
async def registrar(criminal: Criminal):
    try:
        criminal_data = criminal.dict()
        doc_id = registrar_criminal(criminal_data)
        return {"id": doc_id, "mensaje": "Criminal registrado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar criminal: {e}")


