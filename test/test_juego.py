"""
Pruebas unitarias para juego.py (Juego, ResultadoRonda).
"""

import pytest
from src.juego import Juego, ResultadoRonda
from src.modelos import Eleccion, Jugador


class JugadorFijo(Jugador):
    """Jugador de prueba que devuelve una elección fija."""
    def __init__(self, nombre: str, eleccion: Eleccion):
        super().__init__(nombre)
        self._eleccion = eleccion

    def elegir(self) -> Eleccion:
        return self._eleccion


class TestJuego:
    """Pruebas para la clase Juego."""

    def test_empate(self):
        """Dos jugadores con la misma elección deben empatar."""
        j1 = JugadorFijo("A", Eleccion.PIEDRA)
        j2 = JugadorFijo("B", Eleccion.PIEDRA)
        juego = Juego(j1, j2)
        resultado = juego.jugar()
        assert isinstance(resultado, ResultadoRonda)
        assert resultado.ganador == "Empate"
        assert resultado.eleccion1 == Eleccion.PIEDRA
        assert resultado.eleccion2 == Eleccion.PIEDRA

    def test_gana_jugador1(self):
        """Piedra vs Tijeras -> gana jugador1."""
        j1 = JugadorFijo("A", Eleccion.PIEDRA)
        j2 = JugadorFijo("B", Eleccion.TIJERAS)
        juego = Juego(j1, j2)
        resultado = juego.jugar()
        assert resultado.ganador == "A"
        assert resultado.eleccion1 == Eleccion.PIEDRA
        assert resultado.eleccion2 == Eleccion.TIJERAS

    def test_gana_jugador2(self):
        """Papel vs Tijeras -> gana jugador2."""
        j1 = JugadorFijo("A", Eleccion.PAPEL)
        j2 = JugadorFijo("B", Eleccion.TIJERAS)
        juego = Juego(j1, j2)
        resultado = juego.jugar()
        assert resultado.ganador == "B"

    def test_reglas_completas(self):
        """Verifica que las reglas cubran todos los casos no empate."""
        # Ganador -> Perdedor
        reglas = {
            Eleccion.PIEDRA: Eleccion.TIJERAS,
            Eleccion.PAPEL: Eleccion.PIEDRA,
            Eleccion.TIJERAS: Eleccion.PAPEL,
        }
        for ganadora, perdedora in reglas.items():
            j1 = JugadorFijo("A", ganadora)
            j2 = JugadorFijo("B", perdedora)
            juego = Juego(j1, j2)
            resultado = juego.jugar()
            assert resultado.ganador == "A"

            #Invertir orden, debe ganar B
            j1_inv = JugadorFijo("A", perdedora)
            j2_inv = JugadorFijo("B", ganadora)
            juego_inv = Juego(j1_inv, j2_inv)
            resultado_inv = juego_inv.jugar()
            assert resultado_inv.ganador == "B"