"""
Modelos: define las elecciones posibles, la clase base
abstracta para jugadores y las implementaciones Humano e IA.
"""

import logging
import random
from abc import ABC, abstractmethod
from enum import Enum

from .excepciones import EleccionInvalidaError

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


class Eleccion(Enum):
    """
    Representa las tres opciones válidas del juego.
    """
    PIEDRA = "piedra"
    PAPEL = "papel"
    TIJERAS = "tijeras"

    def __str__(self) -> str:
        """Devuelve una representación en español."""
        return self.value


class Jugador(ABC):
    """
    Clase abstracta base para cualquier tipo de jugador.

    Atributo:
        nombre: Nombre identificador del jugador (str).
    Método abstracto:
        elegir() -> Eleccion: Obtiene la elección del jugador.
    """
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        logger.debug(f"Jugador creado: {nombre}")

    @abstractmethod
    def elegir(self) -> Eleccion:
        """
        Solicita o genera una elección válida.
        Debe ser implementada por las subclases.
        """
        pass


class JugadorHumano(Jugador):
    """
    Jugador controlado por entrada de teclado.
    """
    def elegir(self) -> Eleccion:
        """
        Muestra un menú y solicita la elección hasta que sea válida.
        Registra en log tanto el intento como posibles entradas inválidas.
        """
        while True:
            try:
                entrada = input(f"{self.nombre}, elige (piedra/papel/tijeras): ").strip().lower()
                logger.debug(f"{self.nombre} ingresó: '{entrada}'")
                #Buscar en el enum por valor
                eleccion = next((e for e in Eleccion if e.value == entrada), None)
                if eleccion is None:
                    raise EleccionInvalidaError(
                        f"'{entrada}' no es una opción válida. Debes elegir: piedra, papel o tijeras."
                    )
                logger.info(f"{self.nombre} eligió {eleccion}")
                return eleccion
            except EleccionInvalidaError as e:
                print(e)  #Mostrar mensaje al usuario
                logger.warning(f"Elección inválida de {self.nombre}: {e}")
                #El bucle continúa hasta que sea válido


class JugadorIA(Jugador):
    """
    Jugador controlado por la máquina que elige al azar de manera uniforme.
    """
    def elegir(self) -> Eleccion:
        """
        Genera una elección aleatoria entre PIEDRA, PAPEL o TIJERAS.
        """
        eleccion = random.choice(list(Eleccion))
        logger.info(f"{self.nombre} (IA) eligió {eleccion}")
        return eleccion