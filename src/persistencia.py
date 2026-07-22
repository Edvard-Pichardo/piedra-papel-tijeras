"""
Módulo de persistencia en archivos JSON para el historial de partidas.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

from .excepciones import HistorialCorruptoError

logger = logging.getLogger(__name__)


class GestorArchivoJSON:
    """
    Utilidades estáticas para guardar y cargar registros de historial
    en un archivo JSON.
    """

    @staticmethod
    def guardar_historial(ruta: Path, registro: Dict[str, Any]) -> None:
        """
        Agrega un nuevo registro al archivo JSON de historial.
        Si el archivo no existe, lo crea con una lista vacía.
        """
        #Crear directorio padre si no existe
        ruta.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Guardando registro en {ruta}")

        #Cargar lista existente o inicializar vacía
        historial: list = []
        if ruta.exists():
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    historial = json.load(f)
            except (json.JSONDecodeError, PermissionError) as e:
                logger.error(f"No se pudo leer el historial existente: {e}")
                raise HistorialCorruptoError(f"El archivo {ruta} está dañado o no es accesible.") from e

        #Agregar el nuevo registro al final
        historial.append(registro)

        #Escribir de vuelta
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=2, ensure_ascii=False)
        logger.info(f"Registro guardado. Total entradas: {len(historial)}")

    @staticmethod
    def cargar_historial(ruta: Path) -> list[Dict[str, Any]]:
        """
        Lee y retorna todo el historial almacenado.
        Si el archivo no existe, retorna una lista vacía.
        Lanza HistorialCorruptoError si el JSON es inválido.
        """
        if not ruta.exists():
            logger.info(f"No se encontró archivo de historial en {ruta}. Se devuelve lista vacía.")
            return []

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
            logger.debug(f"Historial cargado: {len(datos)} registros")
            return datos
        except json.JSONDecodeError as e:
            logger.error(f"Archivo de historial corrupto: {e}")
            raise HistorialCorruptoError(f"El archivo {ruta} contiene JSON inválido.") from e