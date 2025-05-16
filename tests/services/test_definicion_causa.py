import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException

from app.services.definicion_causa import escribir_causa_muerte
from app.models.models import CausaMuerteRequest
from app.firebase.db import EstadoCriminal

# Datos de prueba
criminal_id = "test-id-123"
causa_muerte = "Accidente de tráfico"

# Preparar datos de prueba
@pytest.fixture
def causa_muerte_request():
    return CausaMuerteRequest(criminal_id=criminal_id, causa_muerte=causa_muerte)


"""
1. Simula la base de datos y funciones externas con valores falsos.
2. Llama a escribir_causa_muerte con un objeto preparado.

Verifica que: Se llamaron funciones correctas, el resultado contiene la información esperada,
los datos del criminal se actualizaron correctamente.
"""
@pytest.mark.asyncio
async def test_escribir_causa_muerte_exitoso(causa_muerte_request):
    # Datos mock del criminal
    criminal_mock = {
        "data": {
            "criminal_id": criminal_id,
            "nombre_completo": "John Doe",
            "proceso": EstadoCriminal.PENDIENTE.value,
            "fecha_registro": "2025-05-16T10:00:00"
        },
        "ref": MagicMock()
    }

    # Simular el comportamiento de las funciones mockeadas:
    # obtener_criminal_death_note, actualizar_muerte_deathnote y publish_event

    with patch('app.services.definicion_causa.obtener_criminal_death_note',
               new_callable=AsyncMock, return_value=criminal_mock) as mock_obtener, \
         patch('app.services.definicion_causa.actualizar_muerte_deathnote',
               new_callable=AsyncMock) as mock_actualizar, \
         patch('app.services.definicion_causa.publish_event',
               new_callable=AsyncMock) as mock_publish:

        # Ejecutar función
        resultado = await escribir_causa_muerte(causa_muerte_request)

        # Verificar que se llamaron las funciones correctas
        mock_obtener.assert_called_once_with(criminal_id)
        mock_actualizar.assert_called_once()
        mock_publish.assert_called_once_with("CausaMuerte", criminal_mock["data"])

        # Verificar que el resultado es correcto
        assert "mensaje" in resultado
        assert causa_muerte in resultado["mensaje"]
        assert "John Doe" in resultado["mensaje"]

        # Verificar que los datos se actualizaron correctamente
        criminal_data = mock_actualizar.call_args[0][1]
        assert criminal_data["causa_muerte"] == causa_muerte
        assert criminal_data["proceso"] == EstadoCriminal.ASIGNADO.value

"""
Verifica que se lanza una excepción HTTP 404 cuando el criminal no se encuentra en la Death Note.
"""
@pytest.mark.asyncio
async def test_criminal_no_encontrado(causa_muerte_request):
    # Configurar mock para retornar None (criminal no encontrado)
    with patch('app.services.definicion_causa.obtener_criminal_death_note',
               new_callable=AsyncMock, return_value=None):

        # Verificar que se lanza la excepción correcta
        with pytest.raises(HTTPException) as excinfo:
            await escribir_causa_muerte(causa_muerte_request)

        # Verificar el código de error
        assert excinfo.value.status_code == 400

"""
Verifica si se lanza una excepción HTTP 400 cuando el criminal ya ha sido
ejecutado o no está en estado pendiente.
"""
@pytest.mark.asyncio
async def test_criminal_ya_ejecutado(causa_muerte_request):
    # Datos mock del criminal ya ejecutado
    criminal_mock = {
        "data": {
            "criminal_id": criminal_id,
            "nombre_completo": "John Doe",
            "proceso": EstadoCriminal.MUERTO.value,
            "fecha_registro": "2025-05-16T10:00:00"
        },
        "ref": MagicMock()
    }
    
    # Configurar mock
    with patch('app.services.definicion_causa.obtener_criminal_death_note',
               new_callable=AsyncMock, return_value=criminal_mock):
        
        # Verificar que se lanza la excepción correcta
        with pytest.raises(HTTPException) as excinfo:
            await escribir_causa_muerte(causa_muerte_request)
        
        # Verificar el código de error
        assert excinfo.value.status_code == 400