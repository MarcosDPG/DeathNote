from fastapi import APIRouter, HTTPException, Path, Body, status
from app.models.models import Criminal, CriminalUpdate
from app.firebase.db import (
    registrar_criminal,
    obtener_criminales,
    actualizar_criminal as actualizar_criminal_db  
)

router = APIRouter(prefix="/api/criminales")

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
        criminal.nombre_completo = criminal.nombre_completo.strip().title()
        
        criminal_data = criminal.model_dump()
        doc_id = registrar_criminal(criminal_data)
        return {"id": doc_id, "mensaje": "Criminal registrado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar criminal: {e}")

@router.patch("/{criminal_id}")
async def actualizar_criminal(
    criminal_id: str = Path(..., title="ID del criminal a actualizar"),
    updates: CriminalUpdate = Body(...)
):
    try:
        updates_dict = updates.model_dump(exclude_unset=True)
        
        if not updates_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos válidos para actualizar"
            )

        if "nombre_completo" in updates_dict:
            updates_dict["nombre_completo"] = updates_dict["nombre_completo"].strip().title()

        # Llamada síncrona
        resultado = actualizar_criminal_db(criminal_id, updates_dict)
        
        return {
            "mensaje": "Criminal actualizado exitosamente",
            "datos_actualizados": {
                k: v for k, v in resultado.items() 
                if k in updates_dict or k == "id"
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )