from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeathNoteRequest(BaseModel):
    criminal_id: str

class CausaMuerteRequest(BaseModel):
    criminal_id: str
    causa_muerte: str

class DetallesMuerteRequest(BaseModel):
    criminal_id: str
    detalles_muerte: str

class Criminal(BaseModel):
    nombre_completo: str  
    foto_base64: Optional[str] = Field(default="no_foto")
    estado: str = "vivo"
    registrado_en: str = datetime.utcnow().isoformat()

class CriminalUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    foto_base64: Optional[str] = None