import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException

from app.services.definicion_detalles import escribir_detalles_muerte
from app.models.models import DetallesMuerteRequest
from app.firebase.db import EstadoCriminal

"""
Pruebas unitarias para la función escribir_detalles_muerte en el módulo definicion_detalles.
Esta prueba verifica el comportamiento de la función al escribir detalles de muerte en la Death Note, dejando
ver si se han llamado las funciones correctas con los parámetros correctos y si se manejan y si la
respuesta es la esperada.
"""
@pytest.mark.asyncio
async def test_escribir_detalles_muerte_exitoso():
    request = DetallesMuerteRequest(criminal_id="abc123", detalles_muerte="Cayó por las escaleras")
    criminal_mock = {
        "data": {
            "criminal_id": "abc123",
            "nombre_completo": "John Doe",
            "proceso": EstadoCriminal.ASIGNADO.value,
            "fecha_registro": "2025-05-16T10:00:00"
        },
        "ref": MagicMock()
    }

    with patch('app.services.definicion_detalles.obtener_criminal_death_note', new_callable=AsyncMock, return_value=criminal_mock) as mock_obtener, \
         patch('app.services.definicion_detalles.actualizar_muerte_deathnote', new_callable=AsyncMock) as mock_actualizar, \
         patch('app.services.definicion_detalles.publish_event', new_callable=AsyncMock) as mock_publish:

        response = await escribir_detalles_muerte(request)

        mock_obtener.assert_called_once_with("abc123")
        mock_actualizar.assert_awaited_once_with(criminal_mock["ref"], criminal_mock["data"])
        mock_publish.assert_awaited_once_with("DetallesMuerte", criminal_mock["data"])
        assert "Se han asignado los detalles de muerte" in response["mensaje"]
        assert "Cayó por las escaleras" in response["mensaje"]
        assert "John Doe" in response["mensaje"]

"""
Prueba unitaria para verificar como se maneja el hecho de que el criminal no se encuentre
en la Death Note.
"""
@pytest.mark.asyncio
async def test_escribir_detalles_muerte_criminal_no_encontrado():
    request = DetallesMuerteRequest(criminal_id="abc123", detalles_muerte="Cayó por las escaleras")
    with patch('app.services.definicion_detalles.obtener_criminal_death_note', new_callable=AsyncMock, return_value=None):
        with pytest.raises(HTTPException) as excinfo:
            await escribir_detalles_muerte(request)
        assert excinfo.value.status_code == 400

"""
Prueba unitaria para verificar como se maneja el hecho de que el criminal ya haya sido ejecutado
o no se le haya asignado causa de muerte.
"""
@pytest.mark.asyncio
async def test_escribir_detalles_muerte_estado_invalido():
    request = DetallesMuerteRequest(criminal_id="abc123", detalles_muerte="Cayó por las escaleras")
    # Crear un criminal mock con un estado diferente a ASIGNADO
    criminal_mock = {
        "data": {
            "criminal_id": "abc123",
            "nombre_completo": "John Doe",
            "proceso": EstadoCriminal.MUERTO.value,
            "fecha_registro": "2025-05-16T10:00:00"
        },
        "ref": MagicMock()
    }
    with patch('app.services.definicion_detalles.obtener_criminal_death_note', new_callable=AsyncMock, return_value=criminal_mock):
        with pytest.raises(HTTPException) as excinfo:
            await escribir_detalles_muerte(request)
        assert excinfo.value.status_code == 400