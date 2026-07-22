"""
Punto de entrada de la aplicación.
Inicializa el juego, permite múltiples rondas y muestra estadísticas al final.
"""

import logging
from datetime import datetime
from pathlib import Path

from .config import configurar_logging, ARCHIVO_HISTORIAL
from .modelos import JugadorHumano, JugadorIA
from .juego import Juego
from .persistencia import GestorArchivoJSON
from .estadisticas import GestorEstadisticas

# Configurar logging al importar el módulo (se ejecuta una sola vez)
configurar_logging()
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Ejecuta el bucle principal del juego.
    """
    logger.info("=== Inicio de la aplicación Piedra, Papel o Tijeras ===")
    
    #Crear jugadores
    humano = JugadorHumano("Humano")
    ia = JugadorIA("IA")
    juego = Juego(humano, ia)

    #Gestor de archivos (estático, no necesita instancia pero usamos la clase)
    gestor_json = GestorArchivoJSON()

    try:
        while True:
            #Ejecutar una ronda
            resultado = juego.jugar()

            #Construir registro para el historial
            registro = {
                "fecha": datetime.now().isoformat(),
                "jugador1": {
                    "nombre": humano.nombre,
                    "eleccion": str(resultado.eleccion1)
                },
                "jugador2": {
                    "nombre": ia.nombre,
                    "eleccion": str(resultado.eleccion2)
                },
                "ganador": resultado.ganador  # "Empate" o nombre del jugador
            }

            #Guardar en archivo JSON
            try:
                gestor_json.guardar_historial(ARCHIVO_HISTORIAL, registro)
            except Exception as e:
                logger.error(f"Error al guardar historial: {e}")
                print("No se pudo guardar el historial de esta ronda.")

            #Mostrar resultado en consola
            print(f"\nResultado: {humano.nombre} [{resultado.eleccion1}] vs "
                  f"{ia.nombre} [{resultado.eleccion2}]")
            if resultado.ganador == "Empate":
                print("¡Empate!\n")
            else:
                print(f"¡Ganó {resultado.ganador}!\n")

            # Preguntar si quiere otra ronda
            continuar = input("¿Jugar otra vez? (s/n): ").strip().lower()
            if continuar not in ("s", "si", "sí", "y", "yes"):
                print("¡Gracias por jugar!")
                break

    except KeyboardInterrupt:
        logger.info("Aplicación interrumpida por el usuario (Ctrl+C)")
        print("\n\nJuego terminado manualmente.")
    except Exception as e:
        logger.critical(f"Error inesperado: {e}", exc_info=True)
        print(f"Ocurrió un error inesperado. Revisa los logs en '{ARCHIVO_HISTORIAL.parent}/../logs' para más detalles.")
    finally:
        #Mostrar estadísticas finales
        print("\nEstadísticas de todas las partidas jugadas:")
        gestor_est = GestorEstadisticas(ARCHIVO_HISTORIAL)
        print(gestor_est.victorias_por_jugador())
        print(gestor_est.eleccion_mas_usada())
        print(gestor_est.porcentaje_empates())
        logger.info("** Fin de la aplicación **")