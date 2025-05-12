from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

router = APIRouter(prefix="/ws")

# Conexiones activas de WebSocket
conexiones_activas: set = set()


@router.websocket("/notificaciones")
async def websocket_eventos(websocket: WebSocket):
    await websocket.accept()
    conexiones_activas.add(websocket)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        conexiones_activas.remove(websocket)

# Notificar a todos los clientes conectados sobre la muerte de un criminal
async def notificar_muerte(muerte_criminal: Dict[str, str]):
    for conexion in conexiones_activas:
        await conexion.send_json(muerte_criminal)