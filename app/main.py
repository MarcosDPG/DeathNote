import asyncio
from events.scheduler import recibir_eventos

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from app.api.criminales import router as criminales_router
from app.api.deathnote import router as deathnote_router
from app.sockets.connection_manager import router as sockets_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Escuchar eventos de Redis
    asyncio.create_task(recibir_eventos())

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (en desarrollo)
    allow_methods=["POST", "GET", "OPTIONS"], 
    allow_headers=["*"],
)

app.include_router(criminales_router)  
app.include_router(deathnote_router)
app.include_router(sockets_router)

