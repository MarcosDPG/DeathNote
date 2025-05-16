import json
import aioredis

from fastapi import Depends
from app.firebase import db


def get_redis_client() -> aioredis.Redis:
    return aioredis.Redis(host="redis", port=6379, db=0)

# Publicar eventos en Redis
async def publish_event(event_type: str, data: dict):
    """
    Publica un evento en el canal de Redis.
    :param event_type: Typo del evento.
    :param data: Datos del evento.
    """
    evento = {
        "tipo": event_type,
        "datos": data
    }
    r: aioredis.Redis = get_redis_client()
    # Publicar el evento en el canal "eventos"
    await r.publish("eventos", json.dumps(evento))
    # Registrar el evento en la base de datos
    db.log_event(event_type, data)