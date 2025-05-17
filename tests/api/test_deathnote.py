import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app

client = TestClient(app)

"""
Pruebas para determinar si el endpoint de registro de muertes funciona correctamente.
"""
@pytest.mark.asyncio
@patch('app.api.deathnote.escribir_muerte', new_callable=AsyncMock)
async def test_registrar_nombre(mock_escribir_muerte):
    mock_escribir_muerte.return_value = {"id": "abc123", "mensaje": "John Doe será ejecutado en 40 segundos si no se especifica la causa."}
    response = client.post("/api/deathnote/id/", json={"criminal_id": "abc123"})
    assert response.status_code == 200
    assert response.json()["id"] == "abc123"

"""
Prueba para determinar si el endpoint para establecer la causa de muerte funciona correctamente.
"""
@pytest.mark.asyncio
@patch('app.api.deathnote.escribir_causa_muerte', new_callable=AsyncMock)
async def test_registrar_causa_muerte(mock_escribir_causa_muerte):
    mock_escribir_causa_muerte.return_value = {"mensaje": "Causa asignada"}
    response = client.put("/api/deathnote/causa-muerte/", json={"criminal_id": "abc123", "causa_muerte": "Accidente"})
    assert response.status_code == 200
    assert "mensaje" in response.json()

"""
Prueba para determinar si el endpoint para establecer los detalles de la muerte funciona correctamente.
"""
@pytest.mark.asyncio
@patch('app.api.deathnote.escribir_detalles_muerte', new_callable=AsyncMock)
async def test_registrar_detalles_muerte(mock_escribir_detalles_muerte):
    mock_escribir_detalles_muerte.return_value = {"mensaje": "Detalles asignados"}
    response = client.put("/api/deathnote/detalles/", json={"criminal_id": "abc123", "detalles_muerte": "Detalles"})
    assert response.status_code == 200
    assert "mensaje" in response.json()