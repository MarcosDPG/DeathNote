from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)

"""
Prueba para verificar la correcta obtención de criminales en una lista.
"""
def test_listar_criminales():
    mock_criminales = [
        {
        "id": "1",
        "nombre": "John Doe",
        "estado": "vivo",
        "foto_base64": "no_foto",
        "registrado_en": "2025-05-16T10:00:00"
        }
    ]
    with patch('app.api.criminales.obtener_criminales', return_value=mock_criminales):
        response = client.get("/api/criminales/")
        assert response.status_code == 200
        assert "criminales" in response.json()
        assert response.json()["criminales"][0]["nombre"] == "John Doe"

"""
Prueba para verificar la correcta obtención de un criminal por nombre.
"""
def test_obtener_criminal_encontrado():
    mock_criminal = {
        "id": "1",
        "nombre": "John Doe",
        "estado": "vivo",
        "foto_base64": "no_foto",
        "registrado_en": "2025-05-16T10:00:00"
    }
    with patch('app.api.criminales.obtener_criminales_nombre', return_value=mock_criminal):
        response = client.get("/api/criminales/nombre/John%20Doe")
        assert response.status_code == 200
        assert response.json()["nombre"] == "John Doe"

"""
Prueba para verificar la correcta obtención de un criminal por nombre que no existe.
"""
def test_obtener_criminal_no_encontrado():
    with patch('app.api.criminales.obtener_criminales_nombre', return_value=None):
        response = client.get("/api/criminales/nombre/Desconocido")
        assert response.status_code == 400
        assert response.json()["detail"] == "Criminal no encontrado"

"""
Prueba para verificar la correcta creación de un criminal.
El test simula la creación de un criminal y verifica que se retorne el ID correcto.
"""
def test_registrar_criminal_exitoso():
    mock_id = "1"
    with patch('app.api.criminales.registrar_criminal', return_value=mock_id):
        data = {
            "nombre_completo": "Jane Doe",
            "foto_base64": "no_foto",
            "estado": "vivo",
            "registrado_en": "2025-05-16T10:00:00"
        }
        response = client.post("/api/criminales/registrar", json=data)
        assert response.status_code == 200
        assert response.json()["id"] == mock_id
        assert "Criminal registrado exitosamente" in response.json()["mensaje"]