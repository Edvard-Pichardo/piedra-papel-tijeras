"""
Pruebas unitarias para modelos.py (Eleccion, JugadorHumano, JugadorIA).
"""

import pytest
from src.modelos import Eleccion, JugadorHumano, JugadorIA
from src.excepciones import EleccionInvalidaError


class TestEleccion:
    """Pruebas para el enum Eleccion."""

    def test_valores_correctos(self):
        """Verifica que los valores de Eleccion son las cadenas esperadas."""
        assert Eleccion.PIEDRA.value == "piedra"
        assert Eleccion.PAPEL.value == "papel"
        assert Eleccion.TIJERAS.value == "tijeras"

    def test_str(self):
        """Verifica que str(Eleccion) devuelve el valor en español."""
        assert str(Eleccion.PIEDRA) == "piedra"
        assert str(Eleccion.PAPEL) == "papel"


class TestJugadorHumano:
    """Pruebas para JugadorHumano usando monkeypatch para input."""

    def test_elegir_valida(self, monkeypatch):
        """Simula entrada 'piedra' y verifica que retorna Eleccion.PIEDRA."""
        monkeypatch.setattr("builtins.input", lambda _: "piedra")
        jugador = JugadorHumano("Test")
        assert jugador.elegir() == Eleccion.PIEDRA

    def test_elegir_invalida_luego_valida(self, monkeypatch):
        """Simula entrada inválida seguida de 'papel' y verifica que retorna Eleccion.PAPEL."""
        entradas = ["invalid", "papel"]
        monkeypatch.setattr("builtins.input", lambda _: entradas.pop(0))
        jugador = JugadorHumano("Test")
        #No debe lanzar excepción, sino pedir de nuevo
        eleccion = jugador.elegir()
        assert eleccion == Eleccion.PAPEL

    def test_elegir_mayusculas_espacios(self, monkeypatch):
        """Simula '  PAPEL  ' (espacios y mayúsculas) y verifica que funciona."""
        monkeypatch.setattr("builtins.input", lambda _: "  PAPEL  ")
        jugador = JugadorHumano("Test")
        assert jugador.elegir() == Eleccion.PAPEL


class TestJugadorIA:
    """Pruebas para JugadorIA parcheando random.choice."""

    def test_elegir_devuelve_eleccion(self, monkeypatch):
        """Simula que random.choice devuelve siempre PIEDRA y verifica el tipo."""
        monkeypatch.setattr("random.choice", lambda _: Eleccion.PIEDRA)
        ia = JugadorIA("Bot")
        assert ia.elegir() == Eleccion.PIEDRA