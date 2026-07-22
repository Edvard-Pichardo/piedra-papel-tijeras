<div align="center">

# Piedra, Papel o Tijeras

Juego clásico implementado utilizando Programación Orientada a Objetos (POO), arquitectura modular, persistencia de datos y pruebas unitarias.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Tested_with-Pytest-0A9EDC?style=for-the-badge&logo=pytest)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)

</div>



# Descripción

Este proyecto implementa el popular juego **Piedra, Papel o Tijeras** como una aplicación completamente modular desarrollada en **Python**.

Más allá de reproducir las reglas del juego, el objetivo principal fue aplicar principios de **ingeniería de software**, utilizando una arquitectura organizada y escalable que incorpora:

- Programación Orientada a Objetos (POO).
- Persistencia de partidas.
- Registro de eventos mediante logging.
- Manejo de excepciones personalizadas.
- Estadísticas automáticas.
- Pruebas unitarias.
- Separación entre lógica de negocio e interfaz.



# Características

- Juego clásico Piedra, Papel o Tijeras.
- Oponente controlado por "inteligencia artificial" (no es así, sus elecciones son mediante una función random).
- Estadísticas automáticas de las partidas.
- Persistencia del historial utilizando archivos JSON.
- Arquitectura completamente modular.
- Sistema de logging.
- Excepciones personalizadas.
- Cobertura mediante pruebas unitarias.
- Interfaz gráfica.
- Proyecto empaquetado con `pyproject.toml`.



# Arquitectura del proyecto

```
src/
│
├── config.py
│      Configuración general y logging.
│
├── excepciones.py
│      Excepciones personalizadas.
│
├── modelos.py
│      Modelos y clases principales.
│
├── juego.py
│      Lógica del juego.
│
├── persistencia.py
│      Lectura y escritura del historial en JSON.
│
├── estadisticas.py
│      Cálculo de estadísticas.
│
├── jugador_gui.py
│      Componentes de la interfaz.
│
├── main.py
│      Aplicación en consola.
│
└── main_gui.py
       Punto de entrada de la interfaz gráfica.
```



# Tecnologías

- Python 3.10+
- Biblioteca estándar de Python
- Pytest
- JSON
- Git
- GitHub



# Estructura del repositorio

```
piedra-papel-tijeras/

├── src/
├── test/
├── LICENSE
├── pyproject.toml
└── README.md
```



# Instalación

Clonar el repositorio

```bash
git clone https://github.com/Edvard-Pichardo/piedra-papel-tijeras.git
```

Entrar al proyecto

```bash
cd piedra-papel-tijeras
```

Instalar dependencias (desarrollo)

```bash
pip install -e .[dev]
```



# Ejecutar el proyecto

Versión de consola

```bash
python -m src.main
```

Versión gráfica

```bash
python -m src.main_gui
```



# Ejecutar las pruebas con ``pytest``

```bash
pytest
```



# Flujo del programa

```text
Inicio
   │
   ▼
Crear jugadores
   │
   ▼
Jugador selecciona opción
   │
   ▼
IA genera movimiento
   │
   ▼
Comparar elecciones
   │
   ▼
Mostrar ganador
   │
   ▼
Guardar historial JSON
   │
   ▼
Actualizar estadísticas
   │
   ▼
¿Nueva partida?
```



# Aprendizajes

Durante el desarrollo de este proyecto se pusieron en práctica conocimientos relacionados con:

- Diseño de software.
- Arquitectura modular.
- Persistencia de datos.
- Organización profesional de proyectos Python.
- Automatización mediante pruebas.
- Control de versiones con Git.



# Posibles mejoras

- Registrar varios jugadores.
- Ranking de jugadores.
- "IA" con distintos niveles de dificultad, incluso integrando una IA de verdad.
- Multijugador.
- Interfaz web.
- Base de datos SQLite.
- Empaquetado como aplicación ejecutable.



# Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

Consulta el archivo **LICENSE** para más información.



# Autor

## Edvard Pichardo

**Licenciado en Física**  
Universidad Nacional Autónoma de México (UNAM)

GitHub

https://github.com/Edvard-Pichardo

---

<div align="center">

</div>
