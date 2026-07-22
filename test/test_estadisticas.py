"""
Pruebas unitarias para estadisticas.py (GestorEstadisticas).
"""

import json
import pytest
from src.estadisticas import GestorEstadisticas


@pytest.fixture
def historial_prueba(tmp_path):
    """Crea un archivo de historial con varias partidas de ejemplo."""
    datos = [
        {"jugador1": {"nombre": "Humano", "eleccion": "piedra"},
         "jugador2": {"nombre": "IA", "eleccion": "tijeras"},
         "ganador": "Humano"},
        {"jugador1": {"nombre": "Humano", "eleccion": "papel"},
         "jugador2": {"nombre": "IA", "eleccion": "papel"},
         "ganador": "Empate"},
        {"jugador1": {"nombre": "Humano", "eleccion": "tijeras"},
         "jugador2": {"nombre": "IA", "eleccion": "papel"},
         "ganador": "Humano"},
        {"jugador1": {"nombre": "Humano", "eleccion": "piedra"},
         "jugador2": {"nombre": "IA", "eleccion": "piedra"},
         "ganador": "Empate"},
    ]
    ruta = tmp_path / "historial.json"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f)
    return ruta


class TestGestorEstadisticas:
    """Pruebas para el gestor de estadísticas con datos de ejemplo."""

    def test_victorias_por_jugador(self, historial_prueba):
        gestor = GestorEstadisticas(historial_prueba)
        resultado = gestor.victorias_por_jugador()
        #Debe incluir "Humano: 2" (IA no ganó ninguna)
        assert "Humano: 2" in resultado
        assert "IA" not in resultado.split(":")[0]  # IA no tiene victorias

    def test_eleccion_mas_usada(self, historial_prueba):
        gestor = GestorEstadisticas(historial_prueba)
        resultado = gestor.eleccion_mas_usada()
        #piedra aparece 3 veces (Humano:2, IA:1) -> debe ser la más frecuente
        assert "piedra" in resultado
        assert "3 veces" in resultado

    def test_porcentaje_empates(self, historial_prueba):
        gestor = GestorEstadisticas(historial_prueba)
        resultado = gestor.porcentaje_empates()
        #2 empates de 4 partidas = 50.00%
        assert "50.00%" in resultado
        assert "2 de 4" in resultado

    def test_sin_datos(self, tmp_path):
        """Con archivo vacío debe mostrar mensajes informativos sin fallar."""
        ruta_vacio = tmp_path / "vacio.json"
        ruta_vacio.write_text("[]")
        gestor = GestorEstadisticas(ruta_vacio)
        assert "No hay victorias registradas" in gestor.victorias_por_jugador()
        assert "No hay datos de elecciones" in gestor.eleccion_mas_usada()
        assert "No hay partidas para calcular" in gestor.porcentaje_empates()