"""
Punto de entrada con interfaz gráfica (tkinter).
Incluye botones para ver/ocultar estadísticas, resetear historial y salir.
Al pausar el juego, el área de resultado muestra "Juego pausado".
"""

import logging
from datetime import datetime
from pathlib import Path

import tkinter as tk

from .config import configurar_logging, ARCHIVO_HISTORIAL
from .modelos import Eleccion, JugadorIA
from .juego import Juego
from .jugador_gui import JugadorTkinter
from .persistencia import GestorArchivoJSON
from .estadisticas import GestorEstadisticas

configurar_logging()
logger = logging.getLogger(__name__)


# Paleta de colores
COLOR_FONDO = "#2E2E2E"
COLOR_TEXTO = "#FFFFFF"
COLOR_BOTON = "#1E90FF"
COLOR_BOTON_HOVER = "#1874CD"
COLOR_BOTON_TEXTO = "#FFFFFF"
COLOR_RESULTADO_FONDO = "#3C3C3C"
COLOR_ESTADISTICAS = "#BBBBBB"
FUENTE_TITULO = ("Segoe UI", 18, "bold")
FUENTE_BOTON = ("Segoe UI", 12, "bold")
FUENTE_RESULTADO = ("Segoe UI", 13)
FUENTE_ESTADISTICAS = ("Segoe UI", 10)


class Aplicacion(tk.Tk):
    """Ventana principal con diseño moderno."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Piedra, Papel o Tijeras")
        self.geometry("500x420")
        self.resizable(False, False)
        self.configure(bg=COLOR_FONDO)

        # Jugadores y juego
        self.humano = JugadorTkinter("Humano")
        self.ia = JugadorIA("IA")
        self.juego = Juego(self.humano, self.ia)
        self.gestor_json = GestorArchivoJSON()

        # Estado del toggle de estadísticas y respaldo del texto de resultado
        self.estadisticas_visibles = False
        self.texto_resultado_anterior = ""  # Se inicializa vacío

        # Construir interfaz
        self._crear_widgets()
        logger.info("Interfaz gráfica iniciada.")

    # Construcción de widgets
    def _crear_widgets(self) -> None:
        """Crea y posiciona todos los elementos visuales."""
        # --- Título ---
        lbl_titulo = tk.Label(
            self,
            text="Piedra, Papel o Tijeras",
            font=FUENTE_TITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        )
        lbl_titulo.pack(pady=(25, 10))

        # Frame para botones de juego
        frame_botones = tk.Frame(self, bg=COLOR_FONDO)
        frame_botones.pack(pady=10)

        emojis = {
            Eleccion.PIEDRA: "🪨  Piedra",
            Eleccion.PAPEL: "📄  Papel",
            Eleccion.TIJERAS: "✂️  Tijeras",
        }

        self.botones = {}
        for opcion in Eleccion:
            btn = tk.Button(
                frame_botones,
                text=emojis[opcion],
                font=FUENTE_BOTON,
                fg=COLOR_BOTON_TEXTO,
                bg=COLOR_BOTON,
                activebackground=COLOR_BOTON_HOVER,
                activeforeground=COLOR_BOTON_TEXTO,
                relief="flat",
                borderwidth=0,
                padx=15,
                pady=8,
                cursor="hand2",
                command=lambda e=opcion: self.jugar_ronda(e)
            )
            btn.pack(side=tk.LEFT, padx=10)
            btn.bind("<Enter>", lambda event, b=btn: b.configure(bg=COLOR_BOTON_HOVER))
            btn.bind("<Leave>", lambda event, b=btn: b.configure(bg=COLOR_BOTON))
            self.botones[opcion] = btn

        # Frame de resultado
        frame_resultado = tk.Frame(
            self, bg=COLOR_RESULTADO_FONDO, padx=20, pady=10,
            relief="groove", borderwidth=2
        )
        frame_resultado.pack(pady=20, fill="x", padx=30)

        self.lbl_resultado = tk.Label(
            frame_resultado,
            text="¡Elige una opción!",
            font=FUENTE_RESULTADO,
            fg=COLOR_TEXTO,
            bg=COLOR_RESULTADO_FONDO
        )
        self.lbl_resultado.pack()

        # Frame inferior para botones de control
        frame_inferior = tk.Frame(self, bg=COLOR_FONDO)
        frame_inferior.pack(pady=(20, 5))

        # Botón Ver / Ocultar estadísticas (toggle)
        self.btn_toggle_est = tk.Button(
            frame_inferior,
            text="📊  Ver estadísticas",
            font=("Segoe UI", 10),
            fg=COLOR_TEXTO,
            bg="#555555",
            activebackground="#777777",
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.toggle_estadisticas
        )
        self.btn_toggle_est.pack(side=tk.LEFT, padx=5)
        self.btn_toggle_est.bind("<Enter>", lambda e, b=self.btn_toggle_est: b.configure(bg="#777777"))
        self.btn_toggle_est.bind("<Leave>", lambda e, b=self.btn_toggle_est: b.configure(bg="#555555"))

        # Botón Resetear
        btn_reset = tk.Button(
            frame_inferior,
            text="🔄  Resetear",
            font=("Segoe UI", 10),
            fg=COLOR_TEXTO,
            bg="#555555",
            activebackground="#777777",
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.resetear_estadisticas
        )
        btn_reset.pack(side=tk.LEFT, padx=5)
        btn_reset.bind("<Enter>", lambda e, b=btn_reset: b.configure(bg="#777777"))
        btn_reset.bind("<Leave>", lambda e, b=btn_reset: b.configure(bg="#555555"))

        # Botón Salir
        btn_salir = tk.Button(
            frame_inferior,
            text="🚪  Salir",
            font=("Segoe UI", 10),
            fg=COLOR_TEXTO,
            bg="#555555",
            activebackground="#777777",
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.destroy
        )
        btn_salir.pack(side=tk.LEFT, padx=5)
        btn_salir.bind("<Enter>", lambda e, b=btn_salir: b.configure(bg="#777777"))
        btn_salir.bind("<Leave>", lambda e, b=btn_salir: b.configure(bg="#555555"))

        # Etiqueta de estadísticas (oculta al inicio) 
        self.lbl_estadisticas = tk.Label(
            self,
            text="",
            font=FUENTE_ESTADISTICAS,
            fg=COLOR_ESTADISTICAS,
            bg=COLOR_FONDO,
            justify=tk.LEFT
        )
        self.lbl_estadisticas.pack(pady=(5, 15))

    # Lógica de juego
    def jugar_ronda(self, eleccion_humano: Eleccion) -> None:
        """Ejecuta una ronda y actualiza la etiqueta de resultado."""
        self.humano.seleccionar(eleccion_humano)
        resultado = self.juego.jugar()

        resumen = (
            f"{self.humano.nombre}: {resultado.eleccion1}   vs   "
            f"{self.ia.nombre}: {resultado.eleccion2}\n"
            f"Ganador: {resultado.ganador}"
        )
        self.lbl_resultado.config(text=resumen)

        # Guardar historial
        registro = {
            "fecha": datetime.now().isoformat(),
            "jugador1": {"nombre": self.humano.nombre, "eleccion": str(resultado.eleccion1)},
            "jugador2": {"nombre": self.ia.nombre, "eleccion": str(resultado.eleccion2)},
            "ganador": resultado.ganador,
        }
        try:
            self.gestor_json.guardar_historial(ARCHIVO_HISTORIAL, registro)
        except Exception as e:
            logger.error(f"No se pudo guardar la partida: {e}")

    # Estadísticas y control
    def toggle_estadisticas(self) -> None:
        """
        Alterna entre mostrar y ocultar las estadísticas.
        Si se muestran, pausa el juego y muestra "Juego pausado".
        Si se ocultan, reanuda el juego y restaura el texto anterior.
        """
        if not self.estadisticas_visibles:
            # Guardar el texto actual de resultado para restaurarlo después
            self.texto_resultado_anterior = self.lbl_resultado.cget("text")

            # Mostrar estadísticas
            try:
                gestor = GestorEstadisticas(ARCHIVO_HISTORIAL)
                texto = (
                    gestor.victorias_por_jugador() + "\n"
                    + gestor.eleccion_mas_usada() + "\n"
                    + gestor.porcentaje_empates()
                )
            except Exception:
                logger.exception("Error al generar estadísticas.")
                texto = "No se pudieron cargar las estadísticas."

            self.lbl_estadisticas.config(text=texto)
            self.lbl_resultado.config(text="Juego pausado")
            self.btn_toggle_est.config(text="🔙  Ocultar estadísticas")
            self.estadisticas_visibles = True

            # Desactivar botones de juego
            for btn in self.botones.values():
                btn.config(state=tk.DISABLED)
            logger.info("Estadísticas mostradas, juego pausado.")
        else:
            # Ocultar estadísticas y reanudar
            self.lbl_estadisticas.config(text="")
            self.lbl_resultado.config(text=self.texto_resultado_anterior)
            self.btn_toggle_est.config(text="📊  Ver estadísticas")
            self.estadisticas_visibles = False

            # Reactivar botones de juego
            for btn in self.botones.values():
                btn.config(state=tk.NORMAL)
            logger.info("Estadísticas ocultadas, juego reanudado.")

    def resetear_estadisticas(self) -> None:
        """Elimina el archivo de historial y actualiza la interfaz."""
        try:
            if ARCHIVO_HISTORIAL.exists():
                ARCHIVO_HISTORIAL.unlink()
                logger.info(f"Historial eliminado: {ARCHIVO_HISTORIAL}")
                mensaje = "Historial borrado correctamente."
            else:
                mensaje = "No hay historial que borrar."
        except Exception as e:
            logger.exception("Error al borrar historial.")
            mensaje = "Error al borrar el historial."

        # Si las estadísticas están visibles, las ocultamos y reactivamos el juego
        if self.estadisticas_visibles:
            self.lbl_estadisticas.config(text="")
            self.lbl_resultado.config(text=self.texto_resultado_anterior)
            self.btn_toggle_est.config(text="📊  Ver estadísticas")
            self.estadisticas_visibles = False
            for btn in self.botones.values():
                btn.config(state=tk.NORMAL)

        # Mostrar mensaje de confirmación en la etiqueta de estadísticas
        self.lbl_estadisticas.config(text=mensaje)


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()