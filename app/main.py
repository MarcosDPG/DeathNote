import asyncio
import aioredis

from contextlib import asynccontextmanager
<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
=======
import asyncio
import aioredis
from app.events.scheduler import recibir_eventos

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.api.criminales import router as criminales_router
from app.api.deathnote import router as deathnote_router
from app.sockets.connection_manager import router as sockets_router
from app.events.scheduler import recibir_eventos

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
app.include_router(criminales_router)
app.include_router(deathnote_router)
app.include_router(sockets_router)

def get_redis_client() -> aioredis.Redis:
    return aioredis.Redis(host="redis", port=6379, db=0)
def get_redis_client() -> aioredis.Redis:
    return aioredis.Redis(host="redis", port=6379, db=0)
>>>>>>> cffbe77ba31a96ca3d58e0cf7c22be3e4f65f0c5


<<<<<<< HEAD
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/", response_class=HTMLResponse)
def read_html():
    html_path = Path("public/index.html")
    return HTMLResponse(content=html_path.read_text(), status_code=200)

@app.get("/room", response_class=HTMLResponse)
def read_html():
    html_path = Path("public/room.html")
    return HTMLResponse(content=html_path.read_text(), status_code=200)

@app.get("/office", response_class=HTMLResponse)
def read_html():
    html_path = Path("public/office.html")
    return HTMLResponse(content=html_path.read_text(), status_code=200)
=======
>>>>>>> cffbe77ba31a96ca3d58e0cf7c22be3e4f65f0c5
