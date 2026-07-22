"""
Calcula y presenta métricas sobre el historial.
"""

import logging
from pathlib import Path
from collections import Counter

from .persistencia import GestorArchivoJSON
from .excepciones import HistorialCorruptoError

logger = logging.getLogger(__name__)


class GestorEstadisticas:
    """
    Clase que procesa los datos del historial y genera estadísticas.
    """
    def __init__(self, ruta_historial: Path) -> None:
        self.ruta = ruta_historial
        self.datos: list[dict] = []
        try:
            self.datos = GestorArchivoJSON.cargar_historial(ruta_historial)
        except HistorialCorruptoError:
            #En caso de corrupción, dejamos lista vacía y mostramos error después
            logger.exception("Historial corrupto, estadísticas no disponibles.")
            self.datos = []

    def victorias_por_jugador(self) -> str:
        """
        Retorna un texto con la cantidad de victorias por jugador.
        """
        contador = Counter()
        for partida in self.datos:
            ganador = partida.get("ganador")
            if ganador and ganador != "Empate":
                contador[ganador] += 1
        if not contador:
            return "No hay victorias registradas."
        lineas = ["Victorias por jugador:"]
        for jugador, victorias in contador.most_common():
            lineas.append(f"  - {jugador}: {victorias}")
        return "\n".join(lineas)

    def eleccion_mas_usada(self) -> str:
        """
        Retorna la elección más frecuente en todas las partidas.
        """
        contador = Counter()
        for partida in self.datos:
            for jugador_key in ("jugador1", "jugador2"):
                eleccion = partida.get(jugador_key, {}).get("eleccion")
                if eleccion:
                    contador[eleccion] += 1
        if not contador:
            return "No hay datos de elecciones."
        mas_comun = contador.most_common(1)[0]
        return f"Elección más usada: '{mas_comun[0]}' ({mas_comun[1]} veces)"

    def porcentaje_empates(self) -> str:
        """
        Calcula y retorna el porcentaje de rondas que terminaron en empate.
        """
        total = len(self.datos)
        if total == 0:
            return "No hay partidas para calcular."
        empates = sum(1 for p in self.datos if p.get("ganador") == "Empate")
        porcentaje = (empates / total) * 100
        return f"Porcentaje de empates: {porcentaje:.2f}% ({empates} de {total})"