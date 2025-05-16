from pydantic import BaseModel

class DeathNoteRequest(BaseModel):
    criminal_id: str

class CausaMuerteRequest(BaseModel):
    criminal_id: str
    causa_muerte: str

class DetallesMuerteRequest(BaseModel):
    criminal_id: str
    detalles_muerte: str