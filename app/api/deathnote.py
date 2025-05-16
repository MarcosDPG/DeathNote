from fastapi import APIRouter

from app.models.models import (
    DeathNoteRequest,
    CausaMuerteRequest,
    DetallesMuerteRequest
)

from app.services.registro_muerte import escribir_muerte
from app.services.definicion_causa import escribir_causa_muerte
from app.services.definicion_detalles import escribir_detalles_muerte

router = APIRouter(prefix="/api/deathnote")

@router.post("/id/")
async def registrar_nombre(request: DeathNoteRequest):
    return await escribir_muerte(request)

@router.put("/causa-muerte/")
async def registrar_causa_muerte(request: CausaMuerteRequest):
    return await escribir_causa_muerte(request)

@router.put("/detalles/")
async def registrar_detalles_muerte(request: DetallesMuerteRequest):
    return await escribir_detalles_muerte(request)