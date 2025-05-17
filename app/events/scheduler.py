import asyncio
import json

import aioredis
from datetime import datetime

from app.firebase.db import (
    obtener_criminal_death_note,
    actualizar_muerte_deathnote,
    actualizar_estado_criminal,
    EstadoCriminal
)

from .eventos import publish_event
from app.sockets.connection_manager import notificar_muerte


# Crear un canal de publicación


# Diccinario para almacenar los temporizadores de cada criminal
timers = {}

# Definir los tiempos de espera
TIEMPO_ESPERA_EJECUCION_DEFAULT = 40  # segundos
TIEMPO_ESPERA_EJECUCION_CAUSA = 10  # segundos
TIEMPO_ESPERA_EJECUCION_DETALLES = 40  # segundos

async def recibir_eventos(r: aioredis.Redis):
    # Esperar y recibir eventos del canal
    pubsub = r.pubsub()
# Suscribirse a un canal
    await pubsub.subscribe('eventos')
    while True:
        mensaje = await pubsub.get_message(ignore_subscribe_messages=True)
        if mensaje:
            # Procesar el evento recibido
            evento = json.loads(mensaje['data'])
            tipo_evento = evento['tipo']
            datos = evento['datos']

            # Verificar el tipo de evento y ejecutar la función correspondiente
            # Si el evento es de muerte por defecto, asignar la muerte por defecto
            if tipo_evento == "MuertePorDefecto":
                await asignar_muerte_defecto(datos['criminal_id'])

            # Si el evento es de muerte con causa, asignar la causa de muerte
            elif tipo_evento == "CausaMuerte":
                # Si el criminal ya tiene un temporizador, cancelarlo
                if datos['criminal_id'] in timers:
                    # Cancelar el temporizador si ya existe
                    timers[datos['criminal_id']].cancel()
                await establecer_causa_muerte(datos['criminal_id'])

            # Si el evento es de muerte con detalles, asignar los detalles de muerte
            elif tipo_evento == "DetallesMuerte":
                # Cancelar el temporizador si ya existe
                if datos['criminal_id'] in timers:
                    timers[datos['criminal_id']].cancel()
                # Establecer la causa de muerte con detalles
                await establecer_detalles_muerte(datos['criminal_id'])

            await notificar_muerte(datos)

            await asyncio.sleep(0.5)  # Esperar un .1 segundos antes de volver a comprobar


async def asignar_muerte_defecto(criminal_id: str) -> dict:
    async def task():
        # Simular un retraso de 40 segundos antes
        await asyncio.sleep(TIEMPO_ESPERA_EJECUCION_DEFAULT)
        # Revisar los datos del criminal en la death note
        criminal_info = await obtener_criminal_death_note(criminal_id)
        # Verificar si el criminal existe y su estado es "pendiente"
        if not criminal_info or criminal_info["data"]["proceso"] != EstadoCriminal.PENDIENTE.value:
            return {"error": "El criminal no existe o ya ha sido ejecutado."}

        criminal_data = criminal_info["data"]
        criminal_ref = criminal_info["ref"]

        # Actualizar los datos localmente
        criminal_data["causa_muerte"] = "Ataque al corazón"
        criminal_data["proceso"] = EstadoCriminal.MUERTO.value
        criminal_data["fecha_ejecucion"] = datetime.now().isoformat()

        # Actualizar en la base de datos
        await actualizar_muerte_deathnote(criminal_ref, criminal_data)
        criminal_data["fecha_registro"] = str(criminal_data["fecha_registro"])
        criminal_data["fecha_ejecucion"] = str(criminal_data["fecha_ejecucion"])
        # Actualizar el estado del criminal a muerto en la colección de criminales
        actualizar_estado_criminal(criminal_id)

        await publish_event("MuerteDefecto", criminal_data)
    # Agregar el temporizador al diccionario
    timers[criminal_id] = asyncio.create_task(task())

async def establecer_causa_muerte(criminal_id) -> dict:
    async def task():
        # Esperar 400 segundos antes de asignar la causa de muerte
        await asyncio.sleep(TIEMPO_ESPERA_EJECUCION_CAUSA)

        criminal = await obtener_criminal_death_note(criminal_id)
        criminal_data = criminal["data"]
        criminal_ref = criminal["ref"]

        # En caso de que el criminal tenga un proceso diferente al que se le asignó una causa de muerte, no se ejecuta
        if not criminal_data or criminal_data["proceso"] != EstadoCriminal.ASIGNADO.value:
            return

        criminal_data["proceso"] = EstadoCriminal.MUERTO.value
        criminal_data["fecha_ejecucion"] = datetime.now().isoformat()

        await actualizar_muerte_deathnote(criminal_ref, criminal_data)

        # Actualizar el estado del criminal a muerto en la colección de criminales
        actualizar_estado_criminal(criminal_id)
        criminal_data["fecha_registro"] = str(criminal_data["fecha_registro"])
        criminal_data["fecha_ejecucion"] = str(criminal_data["fecha_ejecucion"])
        # Crear un evento de muerte
        await publish_event("MuerteConCausa", criminal_data)
    timers[criminal_id] = asyncio.create_task(task())

async def establecer_detalles_muerte(criminal_id) -> dict:
    # Esperar 400 segundos antes de asignar los detalles de muerte
    await asyncio.sleep(TIEMPO_ESPERA_EJECUCION_DETALLES)

    criminal = await obtener_criminal_death_note(criminal_id)
    criminal_data = criminal["data"]
    criminal_ref = criminal["ref"]

    # En caso de que el criminal tenga un proceso diferente al que se le asignó una causa de muerte, no se ejecuta
    if not criminal_data or criminal_data["proceso"] != EstadoCriminal.DETALLADO.value:
        return {"error": "El criminal no existe, está en otro proceso o ya ha sido ejecutado."}

    criminal_data["proceso"] = EstadoCriminal.MUERTO.value
    criminal_data["fecha_ejecucion"] = datetime.now().isoformat()

    await actualizar_muerte_deathnote(criminal_ref, criminal_data)
    # Actualizar el estado del criminal a muerto en la colección de criminales
    actualizar_estado_criminal(criminal_id)

    await publish_event("MuerteConDetalles", criminal_data)

