import asyncio
import redis

from sockets.connection_manager import notificar_muerte

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)
# Crear un canal de publicación
pubsub = r.pubsub()
# Suscribirse a un canal
pubsub.subscribe('eventos')

async def recibir_eventos():
    # Esperar y recibir eventos del canal
    while True:
        mensaje = pubsub.get_message(ignore_subscribe_messages=True)
        if mensaje and mensaje['type'] == 'message':
            # Procesar el evento recibido
            notificar_muerte(mensaje['data'])
        await asyncio.sleep(0.1)  # Esperar un segundo antes de volver a comprobar