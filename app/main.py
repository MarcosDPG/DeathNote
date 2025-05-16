import asyncio
import aioredis
from app.events.scheduler import recibir_eventos

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.api.criminales import router as criminales_router
from app.api.deathnote import router as deathnote_router
from app.sockets.connection_manager import router as sockets_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager para la duración de la aplicación.
    """
    # Conectar a Redis
    r = get_redis_client()
    asyncio.create_task(recibir_eventos(r))
    try:
        yield
    finally:
        # Cerrar la conexión a Redis
        await r.close()

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

def get_redis_client() -> aioredis.Redis:
    return aioredis.Redis(host="redis", port=6379, db=0)


