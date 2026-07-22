"""
Pruebas unitarias para persistencia.py (GestorArchivoJSON).
"""

import json
import pytest
from pathlib import Path
from src.persistencia import GestorArchivoJSON
from src.excepciones import HistorialCorruptoError


class TestGestorArchivoJSON:
    """Pruebas para guardar y cargar historial."""

    def test_guardar_archivo_nuevo(self, tmp_path):
        """Guardar un registro en un archivo que no existe debe crearlo."""
        ruta = tmp_path / "historial.json"
        registro = {"jugador1": "Humano", "eleccion": "piedra"}
        GestorArchivoJSON.guardar_historial(ruta, registro)
        assert ruta.exists()
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        assert len(datos) == 1
        assert datos[0]["jugador1"] == "Humano"

    def test_agregar_a_existente(self, tmp_path):
        """Agregar un segundo registro a un archivo ya existente."""
        ruta = tmp_path / "historial.json"
        registro1 = {"ronda": 1}
        registro2 = {"ronda": 2}
        GestorArchivoJSON.guardar_historial(ruta, registro1)
        GestorArchivoJSON.guardar_historial(ruta, registro2)
        datos = GestorArchivoJSON.cargar_historial(ruta)
        assert len(datos) == 2

    def test_cargar_archivo_inexistente(self, tmp_path):
        """Cargar un archivo que no existe debe devolver lista vacía."""
        ruta = tmp_path / "no_existe.json"
        datos = GestorArchivoJSON.cargar_historial(ruta)
        assert datos == []

    def test_cargar_archivo_corrupto(self, tmp_path):
        """Un archivo con contenido no JSON debe lanzar HistorialCorruptoError."""
        ruta = tmp_path / "corrupto.json"
        ruta.write_text("esto no es json")
        with pytest.raises(HistorialCorruptoError):
            GestorArchivoJSON.cargar_historial(ruta)

    def test_guardar_directorio_intermedio(self, tmp_path):
        """Si la ruta contiene directorios inexistentes, debe crearlos."""
        ruta = tmp_path / "sub" / "historial.json"
        registro = {"test": True}
        GestorArchivoJSON.guardar_historial(ruta, registro)
        assert ruta.exists()