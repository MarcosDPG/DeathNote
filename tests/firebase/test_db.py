import pytest
from unittest.mock import patch, MagicMock

from app.firebase.db import (
    registrar_criminal,
    log_event,
    obtener_criminales,
    obtener_criminales_nombre,
    actualizar_estado_criminal,
    escribir_nombre_deathnote,
    actualizar_muerte_deathnote
)

"""
Este test garantiza que se cree un documento en la colección "criminales" y que se devuelva su ID.
"""
def test_registrar_criminal():
    mock_doc_ref = MagicMock()
    mock_doc_ref.id = "abc123"
    # Simula el comportamiento de db.collection(...)
    with patch("app.firebase.db.db.collection") as mock_collection:
        mock_collection.return_value.document.return_value = mock_doc_ref
        result = registrar_criminal({"nombre": "John"})
        assert result == "abc123"
        mock_doc_ref.set.assert_called_once_with({"nombre": "John"})

"""
Este test garantiza que se registre un evento en la colección "events" con el tipo y criminal_id correctos.
"""
def test_log_event():
    mock_doc_ref = MagicMock()
    with patch("app.firebase.db.db.collection") as mock_collection:
        mock_collection.return_value.document.return_value = mock_doc_ref
        log_event("test", {"criminal_id": "abc"})
        args, kwargs = mock_doc_ref.set.call_args
        assert args[0]["type"] == "test"
        assert args[0]["criminal_id"] == "abc"
        assert "timestamp" in args[0]

"""
Este test garantiza que se devuelvan todos los criminales registrados en la colección "criminales".
"""
def test_obtener_criminales():
    mock_doc = MagicMock()
    mock_doc.to_dict.return_value = {"nombre": "Jane"}
    mock_doc.id = "id1"
    with patch("app.firebase.db.db.collection") as mock_collection:
        mock_collection.return_value.stream.return_value = [mock_doc]
        result = obtener_criminales()
        assert result == [{"nombre": "Jane", "id": "id1"}]

"""
Este test garantiza que se devuelvan criminales que coincidan con el nombre y apellido y que cuando se reciban
los datos por parte de firebase, se devuelvan como una lista de diccionarios.
Si no hay resultados, se devuelve None.
"""
def test_obtener_criminales_nombre():
    mock_doc = MagicMock()
    mock_doc.to_dict.return_value = {"nombre": "Jane"}
    mock_doc.id = "id1"
    with patch("app.firebase.db.db.collection") as mock_collection:
        mock_collection.return_value.where.return_value.stream.return_value = [mock_doc]
        result = obtener_criminales_nombre("Jane")
        assert result == [{"nombre": "Jane", "id": "id1"}]

    # Sin resultados
    with patch("app.firebase.db.db.collection") as mock_collection:
        mock_collection.return_value.where.return_value.stream.return_value = []
        result = obtener_criminales_nombre("Jane")
        assert result is None

"""
Prueba que garantiza que se actualice el estado de un criminal a muerto.
"""
def test_actualizar_estado_criminal():
    mock_doc_ref = MagicMock()
    with patch("app.firebase.db.db.collection") as mock_collection:
        mock_collection.return_value.document.return_value = mock_doc_ref
        actualizar_estado_criminal("abc123")
        # Verifica si se ha llamado a la función update con el estado correcto
        mock_doc_ref.update.assert_called_once_with({"estado": "muerto"})

"""
Este test garantiza que se escriba el nombre del criminal en la Death Note y que se devuelvan
los datos pertinentes.
"""
def test_escribir_nombre_deathnote_exitoso():
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = {"nombre_completo": "Jane", "foto_base64": "foto"}
    mock_deathnote_ref = MagicMock()

    with patch("app.firebase.db.db.collection") as mock_collection:
        mock_criminales = MagicMock()
        # Mock criminales.document().get()
        mock_criminales.document.return_value.get.return_value = mock_doc
        # Mock deathnote.where().limit().get() para que no haya sentencia previa
        mock_deathnote = MagicMock()
        mock_deathnote.where.return_value.limit.return_value.get.return_value = []
        mock_deathnote.document.return_value = mock_deathnote_ref

        # El primer collection es "criminales", el segundo es "deathnote"
        mock_collection.side_effect = lambda name: mock_criminales if name == "criminales" else mock_deathnote

        result = escribir_nombre_deathnote("abc123")
        assert result["criminal_id"] == "abc123"
        assert result["nombre_completo"] == "Jane"
        assert result["proceso"] == "pendiente"
        mock_deathnote_ref.set.assert_called_once()

"""
Este test garantiza que se lance un ValueError si el criminal no existe en la base de datos.
"""
def test_escribir_nombre_deathnote_no_existe():
    mock_doc = MagicMock()
    mock_doc.exists = False
    with patch("app.firebase.db.db.collection") as mock_collection:
        mock_collection.return_value.document.return_value.get.return_value = mock_doc
        with pytest.raises(ValueError):
            escribir_nombre_deathnote("abc123")

""""
Este test garantiza que se lance un ValueError si el criminal no tiene una foto registrada.
"""
def test_escribir_nombre_deathnote_sin_foto():
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = {"nombre": "Jane", "foto_base64": "no_foto"}
    with patch("app.firebase.db.db.collection") as mock_collection:
        mock_collection.return_value.document.return_value.get.return_value = mock_doc
        with pytest.raises(ValueError):
            escribir_nombre_deathnote("abc123")

"""
Este test garantiza que se lance un ValueError si el criminal ya ha sido sentenciado.
"""
def test_escribir_nombre_deathnote_ya_sentenciado():
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = {"nombre": "Jane", "foto_base64": "foto"}
    with patch("app.firebase.db.db.collection") as mock_collection:
        mock_collection.return_value.document.return_value.get.return_value = mock_doc
        mock_collection.return_value.where.return_value.limit.return_value.get.return_value = [MagicMock()]
        with pytest.raises(ValueError):
            escribir_nombre_deathnote("abc123")

"""
Este test garantiza que se utilice la referencia correcta para actualizar la muerte en la Death Note.
"""
@pytest.mark.asyncio
async def test_actualizar_muerte_deathnote():
    mock_ref = MagicMock()
    datos = {"proceso": "muerto"}
    await actualizar_muerte_deathnote(mock_ref, datos)
    mock_ref.update.assert_called_once_with(datos)