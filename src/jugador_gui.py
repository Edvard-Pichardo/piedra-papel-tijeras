"""
Jugador que recibe su elección desde una interfaz gráfica (tkinter).
"""

import logging
from typing import Optional

from .modelos import Eleccion, Jugador

logger = logging.getLogger(__name__)


class JugadorTkinter(Jugador):
    """
    Jugador humano que obtiene su elección por medio de eventos de GUI.

    La clase externa (la ventana) debe llamar a `seleccionar(eleccion)`
    justo antes de ejecutar una ronda, para que `elegir()` pueda retornarla.
    """
    def __init__(self, nombre: str) -> None:
        super().__init__(nombre)
        self._eleccion: Optional[Eleccion] = None

    def seleccionar(self, eleccion: Eleccion) -> None:
        """
        Establece la elección actual del jugador.
        Será consumida por elegir() en la siguiente ronda.
        """
        self._eleccion = eleccion
        logger.debug(f"{self.nombre}: selección GUI establecida -> {eleccion}")

    def elegir(self) -> Eleccion:
        """
        Retorna la elección previamente establecida y la resetea para la
        siguiente ronda. Se asume que siempre se llama a seleccionar() antes.
        """
        if self._eleccion is None:
            #Esto no debería ocurrir si el flujo de la GUI está bien diseñado.
            logger.error(f"{self.nombre}: se llamó a elegir() sin haber seleccionado.")
            raise RuntimeError("No se ha seleccionado ninguna elección en la GUI.")
        eleccion = self._eleccion
        self._eleccion = None   #Reset para la próxima ronda
        return eleccion