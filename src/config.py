"""
Módulo de configuración centralizada.

Define las constantes y la configuración del sistema de logging
para toda la aplicación. El logging se escribe tanto en consola
como en un archivo rotativo, facilitando la depuración.
"""

import logging
from pathlib import Path

# Definimos las constantes del proyecto

#Ruta de la carpeta donde se almacenarán datos (historial JSON)
DIRECTORIO_DATOS = Path("datos")
#Nombre del archivo de historial
ARCHIVO_HISTORIAL = DIRECTORIO_DATOS / "historial.json"
#Ruta de la carpeta de logs
DIRECTORIO_LOGS = Path("logs")
ARCHIVO_LOG = DIRECTORIO_LOGS / "app.log"

# Configuración de logging

def configurar_logging() -> None:
    """
    Configura el logging raíz para que escriba en consola y archivo,
    con formato estandarizado: timestamp, nivel, módulo, mensaje.
    """
    #Aseguramos de que el directorio de logs exista
    DIRECTORIO_LOGS.mkdir(parents=True, exist_ok=True)

    # Formateador común
    formato = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Manejador de archivo (modo 'a', codificación UTF-8)
    manejador_archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    manejador_archivo.setLevel(logging.DEBUG)  #En archivo guardamos todo
    manejador_archivo.setFormatter(formato)

    # Manejador de consola
    manejador_consola = logging.StreamHandler()
    manejador_consola.setLevel(logging.INFO)
    manejador_consola.setFormatter(formato)

    # Configurar el logger raíz
    logger_raiz = logging.getLogger()
    logger_raiz.setLevel(logging.DEBUG)  #Captura todos los niveles
    logger_raiz.addHandler(manejador_archivo)
    logger_raiz.addHandler(manejador_consola)

    # Mensaje inicial de confirmación
    logging.info("Logging configurado correctamente.")