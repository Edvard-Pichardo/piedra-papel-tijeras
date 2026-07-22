"""
Contiene la clase Juego, encargada de orquestar una ronda
y aplicar las reglas de Piedra, Papel o Tijeras.
"""

import logging
from typing import Optional
from typing import NamedTuple

from .modelos import Eleccion, Jugador

logger = logging.getLogger(__name__)

class ResultadoRonda(NamedTuple):
    eleccion1: Eleccion
    eleccion2: Eleccion
    ganador: Optional[str]  #Nombre del ganador o "Empate"

class Juego:
    """
    Gestiona una partida entre dos jugadores.

    Atributos:
        jugador1, jugador2: Instancias de subclases de Jugador.
    Reglas privadas:
        _REGLAS: diccionario que mapea la elección ganadora -> perdedora.
    """
    _REGLAS = {
        Eleccion.PIEDRA: Eleccion.TIJERAS,
        Eleccion.PAPEL: Eleccion.PIEDRA,
        Eleccion.TIJERAS: Eleccion.PAPEL,
    }

    def __init__(self, jugador1: Jugador, jugador2: Jugador) -> None:
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        logger.debug(f"Juego creado entre {jugador1.nombre} y {jugador2.nombre}")

    def _determinar_ganador(self, eleccion1: Eleccion, eleccion2: Eleccion) -> Optional[Eleccion]:
        """
        Aplica las reglas para saber quién gana.

        Retorna:
            La elección ganadora si hay vencedor, o None si hay empate.
        """
        if eleccion1 == eleccion2:
            return None
        #Si eleccion1 vence a eleccion2 según las reglas
        if self._REGLAS[eleccion1] == eleccion2:
            return eleccion1
        else:
            return eleccion2

    def jugar(self) -> ResultadoRonda:
        """
        Ejecuta una ronda completa.
        Retorna un objeto ResultadoRonda con las elecciones y el ganador.
        """
        logger.info("*** Nueva ronda ***")
        eleccion1 = self.jugador1.elegir()
        eleccion2 = self.jugador2.elegir()

        logger.info(
            f"Jugadas: {self.jugador1.nombre} [{eleccion1}] vs "
            f"{self.jugador2.nombre} [{eleccion2}]"
        )

        resultado_eleccion = self._determinar_ganador(eleccion1, eleccion2)
        if resultado_eleccion is None:
            nombre_ganador = "Empate"
            logger.info("Resultado: Empate")
        else:
            nombre_ganador = self.jugador1.nombre if resultado_eleccion == eleccion1 else self.jugador2.nombre
            logger.info(f"Ganador: {nombre_ganador} con {resultado_eleccion}")

        return ResultadoRonda(eleccion1, eleccion2, nombre_ganador)