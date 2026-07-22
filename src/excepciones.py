"""
Módulo de excepciones propias de la aplicación.

Excepciones personalizadas para la legibilidad del manejo
de errores y el control de los bloques try/except.
"""

class EleccionInvalidaError(ValueError):
    """
    Se lanza cuando un jugador proporciona una elección que no
    está dentro de las permitidas (PIEDRA, PAPEL, TIJERAS).
    """
    def __init__(self, mensaje: str = "La elección ingresada no es válida.") -> None:
        super().__init__(mensaje)


class HistorialCorruptoError(Exception):
    """
    Se lanza cuando el archivo de historial JSON está mal formado
    o contiene datos que no se pueden interpretar correctamente.
    """
    def __init__(self, mensaje: str = "El archivo de historial está corrupto.") -> None:
        super().__init__(mensaje)