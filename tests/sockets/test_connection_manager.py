from fastapi.testclient import TestClient
from app.main import app
from app.sockets.connection_manager import conexiones_activas
client = TestClient(app)

"""
Prueba de la conexión al WebSocket y la recepción de mensajes
"""
def test_websocket_notificaciones():
    size_before = len(conexiones_activas)
    # Conectarse al WebSocket
    with client.websocket_connect("/ws/notificaciones") as websocket:
        # El WebSocket se conecta y permanece abierto esperando mensajes
        websocket.send_json({"test": "ping"})
        assert size_before + 1 <= len(conexiones_activas)