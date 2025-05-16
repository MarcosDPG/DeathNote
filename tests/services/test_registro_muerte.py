import pytest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException

from app.services.registro_muerte import escribir_muerte
from app.models.models import DeathNoteRequest

"""
Tests para el servicio de registro de muerte, crea valores de prueba para la Death Note request
y simula la función de escritura en la base de datos. Revisa si la función de escritura
se llama correctamente y si la función de publicación de eventos se llama con los parámetros correctos.
Finalmente, verifica si la respuesta es la esperada.
"""
@pytest.mark.asyncio
async def test_escribir_muerte_exitoso():
    # Datos de entrada y salida simulados
    request = DeathNoteRequest(criminal_id="abc123")
    resultado_mock = {
        "criminal_id": "abc123",
        "nombre_completo": "John Doe",
        "fecha_registro": "2025-05-16T10:00:00"
    }

    with patch('app.services.registro_muerte.escribir_nombre_deathnote', return_value=resultado_mock) as mock_escribir, \
         patch('app.services.registro_muerte.publish_event', new_callable=AsyncMock) as mock_publish:
        
        response = await escribir_muerte(request)
        
        mock_escribir.assert_called_once_with("abc123")
        mock_publish.assert_awaited_once_with("MuertePorDefecto", resultado_mock)
        assert response["id"] == "abc123"
        assert "será ejecutado en 40 segundos" in response["mensaje"]

"""
Test para el servicio de registro de muerte, simula un error al escribir en la base de datos
y verifica si se lanza una excepción HTTPException con el código de estado 400 y el mensaje de error correspondiente.
"""
@pytest.mark.asyncio
async def test_escribir_muerte_valor_error():
    request = DeathNoteRequest(criminal_id="abc123")
    with patch('app.services.registro_muerte.escribir_nombre_deathnote', side_effect=ValueError("Ya existe")):
        with pytest.raises(HTTPException) as excinfo:
            await escribir_muerte(request)
        assert excinfo.value.status_code == 400
        assert "Ya existe" in str(excinfo.value.detail)